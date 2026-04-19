from .transcripts_handlers.transcript_final_executor import process_transcripts
from ..database_utilities.write_database import insert_dataframe


def feed_transcripts(symbol):
    # 1. Fetch transcripts
    transcripts_df = process_transcripts(symbol)
    
    transcripts_df.columns = ["company", "title", "url", "filepath", "date"]
    
    transcripts_df.rename(columns={"symbol": "company", "title": "title", "url": "url", "filepath": "filepath", "date": "date"}, inplace=True)

    # 2. Insert into database
    insert_dataframe(transcripts_df, "transcripts_2")
