# 🌦️ Weather Forecast Microservice

This is a FastAPI-based microservice that fetches weather data from the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), filters out nighttime periods, and stores the daytime temperature forecasts in a SQLite database.

---

## 🚀 Features

- Fetches and filters daytime weather forecasts using `aiohttp`
- Stores results in a local SQLite database with `aiosqlite`
- Provides two REST API endpoints:
  - `GET /fetch_data` — fetches and stores the latest forecast
  - `GET /results` — retrieves stored forecast data
- Built with Docker, testable with Pytest

---

## 📦 Requirements

- Docker + Docker Compose
- Python 3.11 (used in container)
- (Optional) Makefile for simplified commands

---

## 🔧 Setup

### 1. Build the Docker image

```bash
docker-compose build
```

### 2. Run the application

```bash
docker-compose up
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API.

---

## 🧪 Running Tests

```bash
docker-compose run --rm test
```
---

## 📁 Project Structure

```
app/
├── main.py               # FastAPI application logic
├── db.py                 # Reads results back from the DB
├── fetch.py              # Fetching, Filtering, and Saving results to DB
├── api.json              # Sample API response (optional for testing)
├── test_forecast.py      # Pytest test suite
├── data.db               # SQLite DB (created after POST /update)
├── requirements.txt
Dockerfile
docker-compose.yml
```

---

## 🛠 Endpoints
Run docker and navigate to these endpoints on your localhost.

### `GET /fetch_data`

Fetches data from the external API, filters out night entries, and stores:

```json
[
  {
    "startTime": "2025-04-22T06:00:00-04:00",
    "temperature": 88
  },
  ...
]
```

### `GET /results`

Returns the stored forecast from the SQLite database.

---

## 🧹 Dev Tips

- If the database schema changes, delete `data.db` and re-run `/update`
- Rebuild with `--no-cache` if changes to `requirements.txt` aren't picked up

---

## 📄 License

MIT — use freely, credit appreciated.
