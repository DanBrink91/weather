from fastapi import FastAPI, HTTPException
from fetch import fetch_and_store_data
from db import get_stored_data

app = FastAPI()

@app.get("/fetch_data")
async def fetch_data():
    try:
        await fetch_and_store_data()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f'{str(e)}')
    return {"status": "Data updated and stored."}

@app.get("/results")
async def results():
    try:
        data = await get_stored_data()
    except HTTPException as e:
        raise e
    return {"data": data}
