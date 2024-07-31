from fastapi import FastAPI
from data_fetch import fetch_and_process_data
from converter import convert_to_protobuf
from producer import send_to_kafka
import os

app = FastAPI()

@app.post("/fetch-data/")
async def fetch_data(jurisdiction: str, report_type: str, asset_class: str, start_date: str, end_date: str):
    urls = gen_urls(start_date, end_date, jurisdiction, report_type, asset_class)
    dfs = await fetch_and_process_data(urls)
    return {"status": "data fetched", "dataframes": len(dfs)}

@app.post("/convert/")
def convert(data):
    protobuf_data = convert_to_protobuf(data)
    return {"status": "data converted"}

@app.post("/send/")
def send(data):
    send_to_kafka(data)
    return {"status": "data sent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
