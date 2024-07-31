from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data_fetch import fetch_and_process_data
from converter import convert_to_protobuf
from producer import kafka_handler
from os import getenv

app = FastAPI()

class DataRequest(BaseModel):
    jurisdiction: str
    report_type: str
    asset_class: str
    start_date: str
    end_date: str

@app.post("/fetch-data/")
async def fetch_data(request: DataRequest):
    urls = gen_urls(request.start_date, request.end_date, request.jurisdiction, request.report_type, request.asset_class)
    try:
        dfs = await fetch_and_process_data(urls)
        return {"status": "data fetched", "dataframes": len(dfs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/")
async def convert(data: bytes):
    try:
        protobuf_data = convert_to_protobuf(data)
        return {"status": "data converted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send/")
async def send(data: bytes, topic: str):
    try:
        kafka_handler.send(data, topic)
        return {"status": "data sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(getenv("PORT", 8000)))
