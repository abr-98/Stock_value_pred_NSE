"""
User/account router with JWT auth, chat threads, token tracking, watchlist, and portfolio APIs.
"""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional

import jwt
import psycopg2
import tiktoken
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from apis.logging_config import setup_logging, log_service_io
from apis.models.schemas import (
    ErrorResponse,
    LoginRequest,
    MessageCreateRequest,
    MessageCreateResponse,
    MessageResponse,
    PortfolioCreateRequest,
    PortfolioResponse,
    ThreadCreateRequest,
    ThreadResponse,
    TokenUsageAggregateResponse,
    TokenUsageRecordResponse,
    UserAuthResponse,
    UserProfileResponse,
    UserRegisterRequest,
    WatchlistCreateRequest,
    WatchlistResponse,
)

router = APIRouter()
logger = setup_logging("service-user-router")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-jwt-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = int(os.environ.get("JWT_EXPIRE_HOURS", "24"))
PASSWORD_SALT = os.environ.get("PASSWORD_SALT", "dev-password-salt")

MODEL_PRICING_PER_1M = {
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def _get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="Stock_database",
        user="postgres",
        password="1234",
        port=5432,
    )


def _hash_password(password: str) -> str:
    material = f"{PASSWORD_SALT}:{password}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def _verify_password(password: str, password_hash: str) -> bool:
    return _hash_password(password) == password_hash


def _create_access_token(user_id: int, email: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "email": email, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def _count_tokens(text: str, model: str) -> int:
    model_name = model or "gpt-4o"
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text or ""))


def _estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    pricing = MODEL_PRICING_PER_1M.get(model, MODEL_PRICING_PER_1M["gpt-4o-mini"])
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(float(input_cost + output_cost), 8)


def _fetch_user_by_email(email: str) -> Optional[tuple]:
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, email, password_hash, plan_type, token_usage, created_at FROM users WHERE email = %s",
            (email.lower().strip(),),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def _fetch_user_by_id(user_id: int) -> Optional[tuple]:
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, email, plan_type, token_usage, created_at FROM users WHERE id = %s",
            (user_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def _require_thread_owner(thread_id: int, user_id: int):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM chat_threads WHERE id = %s AND user_id = %s", (thread_id, user_id))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Thread not found")
    finally:
        cur.close()
        conn.close()


def _require_row(row, message: str):
    if row is None:
        raise HTTPException(status_code=500, detail=message)
    return row


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = _decode_token(token)
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = _fetch_user_by_id(int(user_id_raw))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {
        "id": user[0],
        "email": user[1],
        "plan_type": user[2],
        "token_usage": int(user[3] or 0),
        "created_at": user[4],
    }


@router.post(
    "/register",
    response_model=UserAuthResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Register user",
)
def register_user(request: UserRegisterRequest):
    log_service_io(logger, "users.register.request", inputs={"email": request.email})

    existing = _fetch_user_by_email(request.email)
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (email, password_hash, plan_type)
            VALUES (%s, %s, %s)
            RETURNING id, email, plan_type, token_usage, created_at
            """,
            (
                request.email.lower().strip(),
                _hash_password(request.password),
                request.plan_type or "free",
            ),
        )
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    row = _require_row(row, "Failed to create user")

    token = _create_access_token(row[0], row[1])
    return UserAuthResponse(
        status="success",
        access_token=token,
        token_type="bearer",
        user=UserProfileResponse(
            id=row[0],
            email=row[1],
            plan_type=row[2],
            token_usage=int(row[3] or 0),
            created_at=row[4],
        ),
    )


@router.post(
    "/login",
    response_model=UserAuthResponse,
    responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Login user",
)
def login_user(request: LoginRequest):
    log_service_io(logger, "users.login.request", inputs={"email": request.email})

    user = _fetch_user_by_email(request.email)
    if user is None or not _verify_password(request.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = _create_access_token(user[0], user[1])
    return UserAuthResponse(
        status="success",
        access_token=token,
        token_type="bearer",
        user=UserProfileResponse(
            id=user[0],
            email=user[1],
            plan_type=user[3],
            token_usage=int(user[4] or 0),
            created_at=user[5],
        ),
    )


@router.get("/me", response_model=UserProfileResponse, summary="Get current user profile")
def get_me(current_user: dict = Depends(get_current_user)):
    return UserProfileResponse(**current_user)


@router.post("/threads", response_model=ThreadResponse, summary="Create chat thread")
def create_thread(request: ThreadCreateRequest, current_user: dict = Depends(get_current_user)):
    title = (request.title or "").strip() or "New Chat"

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO chat_threads (user_id, title)
            VALUES (%s, %s)
            RETURNING id, user_id, title, created_at
            """,
            (current_user["id"], title),
        )
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    row = _require_row(row, "Failed to create thread")

    return ThreadResponse(id=row[0], user_id=row[1], title=row[2], created_at=row[3])


@router.get("/threads", response_model=list[ThreadResponse], summary="List user chat threads")
def list_threads(current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, user_id, title, created_at FROM chat_threads WHERE user_id = %s ORDER BY created_at DESC",
            (current_user["id"],),
        )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return [ThreadResponse(id=r[0], user_id=r[1], title=r[2], created_at=r[3]) for r in rows]


@router.get("/threads/{thread_id}/messages", response_model=list[MessageResponse], summary="List thread messages")
def list_messages(thread_id: int, current_user: dict = Depends(get_current_user)):
    _require_thread_owner(thread_id, current_user["id"])

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, thread_id, role, content, token_count, model, created_at
            FROM messages
            WHERE thread_id = %s
            ORDER BY created_at ASC
            """,
            (thread_id,),
        )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return [
        MessageResponse(
            id=r[0],
            thread_id=r[1],
            role=r[2],
            content=r[3],
            token_count=int(r[4] or 0),
            model=r[5],
            created_at=r[6],
        )
        for r in rows
    ]


@router.post(
    "/threads/{thread_id}/messages",
    response_model=MessageCreateResponse,
    summary="Create message and track token usage",
)
def create_message(
    thread_id: int,
    request: MessageCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    _require_thread_owner(thread_id, current_user["id"])

    model = request.model or "gpt-4o"
    token_count = _count_tokens(request.content, model)

    if request.input_tokens is not None or request.output_tokens is not None:
        input_tokens = int(request.input_tokens or 0)
        output_tokens = int(request.output_tokens or 0)
    else:
        if request.role == "assistant":
            input_tokens = 0
            output_tokens = token_count
        else:
            input_tokens = token_count
            output_tokens = 0

    total_tokens = int(input_tokens + output_tokens)
    cost = _estimate_cost(input_tokens, output_tokens, model)

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO messages (thread_id, role, content, token_count, model)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, thread_id, role, content, token_count, model, created_at
            """,
            (thread_id, request.role, request.content, token_count, model),
        )
        msg = cur.fetchone()

        cur.execute(
            """
            INSERT INTO token_usage (user_id, thread_id, input_tokens, output_tokens, total_tokens, model, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, user_id, thread_id, input_tokens, output_tokens, total_tokens, model, cost, timestamp
            """,
            (current_user["id"], thread_id, input_tokens, output_tokens, total_tokens, model, Decimal(str(cost))),
        )
        usage = cur.fetchone()

        cur.execute(
            "UPDATE users SET token_usage = COALESCE(token_usage, 0) + %s WHERE id = %s",
            (total_tokens, current_user["id"]),
        )

        conn.commit()
    finally:
        cur.close()
        conn.close()

    msg = _require_row(msg, "Failed to create message")
    usage = _require_row(usage, "Failed to write token usage")

    return MessageCreateResponse(
        status="success",
        message=MessageResponse(
            id=msg[0],
            thread_id=msg[1],
            role=msg[2],
            content=msg[3],
            token_count=int(msg[4] or 0),
            model=msg[5],
            created_at=msg[6],
        ),
        usage=TokenUsageRecordResponse(
            id=usage[0],
            user_id=usage[1],
            thread_id=usage[2],
            input_tokens=int(usage[3] or 0),
            output_tokens=int(usage[4] or 0),
            total_tokens=int(usage[5] or 0),
            model=usage[6],
            cost=float(usage[7] or 0),
            timestamp=usage[8],
        ),
    )


@router.get("/token-usage", response_model=TokenUsageAggregateResponse, summary="Get token usage summary")
def get_token_usage(current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT
                COALESCE(SUM(input_tokens), 0),
                COALESCE(SUM(output_tokens), 0),
                COALESCE(SUM(total_tokens), 0),
                COALESCE(SUM(cost), 0)
            FROM token_usage
            WHERE user_id = %s
            """,
            (current_user["id"],),
        )
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    row = row or (0, 0, 0, 0)

    return TokenUsageAggregateResponse(
        user_id=current_user["id"],
        input_tokens=int(row[0] or 0),
        output_tokens=int(row[1] or 0),
        total_tokens=int(row[2] or 0),
        total_cost=float(row[3] or 0),
    )


@router.post("/watchlist", response_model=WatchlistResponse, summary="Add ticker to watchlist")
def add_watchlist(request: WatchlistCreateRequest, current_user: dict = Depends(get_current_user)):
    ticker = request.ticker.upper().strip()
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO watchlists (user_id, ticker)
            VALUES (%s, %s)
            ON CONFLICT (user_id, ticker) DO UPDATE SET ticker = EXCLUDED.ticker
            RETURNING id, user_id, ticker, added_at
            """,
            (current_user["id"], ticker),
        )
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    row = _require_row(row, "Failed to add watchlist item")

    return WatchlistResponse(id=row[0], user_id=row[1], ticker=row[2], added_at=row[3])


@router.get("/watchlist", response_model=list[WatchlistResponse], summary="List watchlist")
def list_watchlist(current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, user_id, ticker, added_at FROM watchlists WHERE user_id = %s ORDER BY added_at DESC",
            (current_user["id"],),
        )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return [WatchlistResponse(id=r[0], user_id=r[1], ticker=r[2], added_at=r[3]) for r in rows]


@router.delete("/watchlist/{ticker}", summary="Remove ticker from watchlist")
def delete_watchlist(ticker: str, current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM watchlists WHERE user_id = %s AND ticker = %s",
            (current_user["id"], ticker.upper().strip()),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return {"status": "success", "ticker": ticker.upper().strip()}


@router.post("/portfolio", response_model=PortfolioResponse, summary="Add/update portfolio position")
def add_portfolio(request: PortfolioCreateRequest, current_user: dict = Depends(get_current_user)):
    ticker = request.ticker.upper().strip()

    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO portfolios (user_id, ticker, quantity, avg_buy_price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, ticker)
            DO UPDATE SET quantity = EXCLUDED.quantity, avg_buy_price = EXCLUDED.avg_buy_price
            RETURNING id, user_id, ticker, quantity, avg_buy_price, created_at
            """,
            (current_user["id"], ticker, request.quantity, request.avg_buy_price),
        )
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    row = _require_row(row, "Failed to add portfolio position")

    return PortfolioResponse(
        id=row[0],
        user_id=row[1],
        ticker=row[2],
        quantity=float(row[3]),
        avg_buy_price=float(row[4]),
        created_at=row[5],
    )


@router.get("/portfolio", response_model=list[PortfolioResponse], summary="List portfolio positions")
def list_portfolio(current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, user_id, ticker, quantity, avg_buy_price, created_at FROM portfolios WHERE user_id = %s ORDER BY created_at DESC",
            (current_user["id"],),
        )
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return [
        PortfolioResponse(
            id=r[0],
            user_id=r[1],
            ticker=r[2],
            quantity=float(r[3]),
            avg_buy_price=float(r[4]),
            created_at=r[5],
        )
        for r in rows
    ]


@router.delete("/portfolio/{ticker}", summary="Remove portfolio position")
def delete_portfolio(ticker: str, current_user: dict = Depends(get_current_user)):
    conn = _get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM portfolios WHERE user_id = %s AND ticker = %s",
            (current_user["id"], ticker.upper().strip()),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return {"status": "success", "ticker": ticker.upper().strip()}
