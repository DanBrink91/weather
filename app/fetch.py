from fastapi import HTTPException
import aiohttp
import asyncio
import pandas as pd
import aiosqlite
import io

API_URL = "	https://api.weather.gov/gridpoints/MLB/31,80/forecast"

async def extract_daytime_forecast(json_data):
    try:
        periods = json_data['properties']['periods']
    except (KeyError, TypeError):
        raise ValueError("Invalid API structure — could not find 'properties.periods'")
     # Load into DataFrame
    df = pd.DataFrame(periods)

    if "name" not in df or "startTime" not in df or "temperature" not in df:
        raise ValueError("Missing expected columns in data")

    # Filter out rows with 'night' in the 'name' field (case-insensitive)
    mask = ~df["name"].str.lower().str.contains("night", na=False)
    df_filtered = df[mask][["startTime", "temperature"]]

    # Drop rows with nulls and validate types
    df_filtered = df_filtered.dropna(subset=["startTime", "temperature"])

    return df_filtered.to_dict(orient="records")

# Remove the days that match the maximum temperature
async def eliminate_max_temperatures(forecast):
    df = pd.DataFrame(forecast)

    max_temp_value = df['temperature'].max()
    return df[df['temperature'] != max_temp_value]

async def fetch_and_store_data():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, timeout=10) as response:
                json_data = await response.json()
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=502, detail=f"API request failed: {str(e)}")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=502, detail=f"API request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    try:
        forecast = await extract_daytime_forecast(json_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid API structure — could not find 'properties.periods'")
    
    # Remove the days that match the maximum temperature
    filtered_df = await eliminate_max_temperatures(forecast)

    # Save dataframe to a buffer in memory
    buffer = io.StringIO()
    filtered_df.to_csv(buffer, index=False)
    buffer.seek(0)
    try:
        # Store using aiosqlite
        async with aiosqlite.connect("data.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    Date DATE PRIMARY KEY,
                    Temperature INT
                )
            """)
            for _, row in filtered_df.iterrows():
                await db.execute("""
                    INSERT OR REPLACE INTO weather (Temperature, Date)
                    VALUES (?, ?)
                """, tuple([row['temperature'], row['startTime']]))
            await db.commit()
    except aiosqlite.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

