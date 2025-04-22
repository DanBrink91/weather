import aiosqlite
from fastapi import HTTPException


async def get_stored_data():
    results = []
    try:
        async with aiosqlite.connect("data.db") as db:
            async with db.execute("SELECT * FROM weather") as cursor:
                async for row in cursor:
                    results.append({
                        "Date": row[0],
                        "Temperature": row[1]
                    })
    except aiosqlite.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to read from database: {str(e)}")
    return results
