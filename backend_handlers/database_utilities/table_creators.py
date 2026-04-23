import psycopg2


def create():
    conn = psycopg2.connect(host="localhost",
                            database= "Stock_database",
                            user="postgres",
                            password="1234",
                            port="5432")

    cur = conn.cursor()

    try:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS news_2 (
                        id SERIAL PRIMARY KEY,
                        company VARCHAR(255),
                        title TEXT,
                        url TEXT,
                        year INT,
                        month INT,
                        day INT,
                        UNIQUE(title, url)
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS transcripts_3 (
                        id SERIAL PRIMARY KEY,
                        company VARCHAR(255),
                        title TEXT,
                        url TEXT,
                        filepath TEXT,
                        date DATE,
                        UNIQUE(title, url)
                    )
                    """)


        cur.execute("""
                    CREATE TABLE IF NOT EXISTS top_gainers_2 (
                        sector VARCHAR(255),
                        company VARCHAR(255),
                        pCHANGE FLOAT,
                        date DATE,
                        UNIQUE(sector, company, date)
                    )
                    """)
        
        conn.commit()
    except Exception as e:
        print("Error creating tables:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()