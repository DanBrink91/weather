import pytest
import asyncio
import pytest_asyncio
from fetch import extract_daytime_forecast

@pytest.mark.asyncio
async def test_extract_daytime_forecast_valid():
    mock_data = {
        "properties": {
            "periods": [
                {"name": "Monday", "startTime": "2025-04-21T08:00", "temperature": 85},
                {"name": "Monday Night", "startTime": "2025-04-21T20:00", "temperature": 65},
                {"name": "Tuesday", "startTime": "2025-04-22T08:00", "temperature": 88},
            ]
        }
    }

    result = await extract_daytime_forecast(mock_data)
    assert result == [
        {"startTime": "2025-04-21T08:00", "temperature": 85},
        {"startTime": "2025-04-22T08:00", "temperature": 88}
    ]

@pytest.mark.asyncio
async def test_night_case_insensitivity():
    mock_data = {
        "properties": {
            "periods": [
                {"name": "Night", "startTime": "time1", "temperature": 1},
                {"name": "NIGHT", "startTime": "time2", "temperature": 2},
                {"name": "Saturday", "startTime": "time3", "temperature": 3}
            ]
        }
    }

    result = await extract_daytime_forecast(mock_data)
    assert result == [{"startTime": "time3", "temperature": 3}]

@pytest.mark.asyncio
async def test_extract_forecast_missing_properties():
    with pytest.raises(ValueError, match="Invalid API structure"):
        await extract_daytime_forecast({})

@pytest.mark.asyncio
async def test_only_night_entries():
    mock_data = {
        "properties": {
            "periods": [
                {"name": "Monday Night", "startTime": "night1", "temperature": 55}
            ]
        }
    }

    result = await extract_daytime_forecast(mock_data)
    assert result == []

@pytest.mark.asyncio
async def test_missing_fields():
    mock_data = {
        "properties": {
            "periods": [
                {"name": "Monday", "startTime": "t1"},  # missing temperature
                {"name": "Tuesday", "temperature": 85}, # missing startTime
            ]
        }
    }

    result = await extract_daytime_forecast(mock_data)
    assert result == []
