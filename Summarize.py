import os
from pathlib import Path
import pandas as pd
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_long_text(text, max_chunk_len=1024):
    chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks if chunk.strip()]
    return ' '.join(summaries)

folder_path = "./WebCrawler/"

csv_files = list(Path(folder_path).glob("*.csv"))
summary_data = []

for file in csv_files:
    try:
        df = pd.read_csv(file)
        if "EV_Content" in df.columns:
            all_text = ' '.join(df["EV_Content"].dropna().astype(str))
            summary = summarize_long_text(all_text)
            summary_data.append({"File_Name": file.name, "EV_Summary": summary})
    except Exception as e:
        summary_data.append({"File_Name": file.name, "EV_Summary": f"Error: {e}"})

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv("ev_summary_report.csv", index=False, encoding="utf-8")
