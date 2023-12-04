import logging
import os
from datetime import datetime
import uvicorn
from bson import json_util
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Security, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

description = ""
with open("static/description.md", "r") as file:
  for line in file:
    description += line

app = FastAPI(title="Arduino temp API", description=description)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Set up logging
logging.basicConfig(level=logging.INFO)
connection_string = os.environ["mongodb_connection_string"]
# Use the primary connection string directly
client = AsyncIOMotorClient(connection_string)
db = client['temp-data']  # Using the 'temp-data' database
temperature_collection = db[
    'collection-1']  # Using the 'collection-1' collection

arduino_api_key = os.environ['ARDUINO_TEMP_API_KEY']
api_keys = [arduino_api_key]
api_key_header = APIKeyHeader(name="arduino-temp-api", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header), ) -> str:
  if api_key_header in api_keys:
    return api_key_header
  raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or missing API Key",
  )


# Helper function to determine temperature category and LED color
def determine_temp_category_and_led_color(temperature):
  if 15 <= temperature < 40:
    return "stabil", "grön"
  elif temperature < 15:
    return "låg", "blå"
  else:
    return "hög", "röd"


@app.get("/privacy-policy", response_class=HTMLResponse, tags=["webpages"])
async def privacy_policy(request: Request):
  return templates.TemplateResponse("privacy-policy.html",
                                    {"request": request})


@app.get('/', response_class=HTMLResponse, tags=["webpages"])
async def index_page(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@app.post("/temperature/insert_data", tags=["POST endpoints"])
async def receive_temperature(request: Request,
                              api_key: str = Security(get_api_key)):
  data = await request.json()  # Use 'await' for asynchronous call
  temperature = data.get("temperature")
  import pytz
  stockholm_tz = pytz.timezone('Europe/Stockholm')
  timestamp = datetime.now(stockholm_tz).strftime('%Y-%m-%d %H:%M:%S.%f')

  # Determine temperature category and LED color
  temp_category, led_color = determine_temp_category_and_led_color(temperature)

  # Log the temperature, timestamp, and category
  logging.info(
      f"Received temperature: {temperature} C, Category: {temp_category}, LED: {led_color}, Timestamp: {timestamp}"
  )

  # Insert data into MongoDB asynchronously
  document_to_insert = {
      "temperature": temperature,
      "tempCategory": temp_category,
      "ledColor": led_color,
      "timestamp": timestamp
  }
  insert_result = await temperature_collection.insert_one(
      document_to_insert)  # Use 'await' for async insert
  logging.info(f"Data inserted with id {insert_result.inserted_id}")

  return JSONResponse(
      content={
          "message": "Data received and inserted successfully",
          "id": str(insert_result.inserted_id)
      })


@app.get("/temperature/fetch_data", tags=["GET endpoints"])
async def get_items(limit: int = 10):
  cursor = temperature_collection.find().sort("_id", -1).limit(limit)
  items = [doc async for doc in cursor]  # Asynchronously iterate over cursor
  return JSONResponse(content=json_util.dumps(items))


@app.get("/temperature/by_category", tags=["GET endpoints"])
async def get_temperatures_by_category(category: str):
  # Normalize the category input to ensure consistency
  normalized_category = category.lower()

  # Check if the category is valid
  if normalized_category not in ["låg", "hög", "stabil"]:
    return JSONResponse(
        status_code=400,
        content={
            "message":
            "Invalid category. Allowed categories are 'låg', 'hög', or 'stabil'."
        })

  # Fetch data based on the category
  cursor = temperature_collection.find({
      "tempCategory": normalized_category
  }).sort("_id", -1)
  items = [doc async for doc in cursor]
  return JSONResponse(content=json_util.dumps(items))


from datetime import datetime, timedelta


@app.get("/temperature/time_interval", tags=["GET endpoints"])
async def get_data_by_time_interval(interval: str, amount: int):
  # Current time
  current_time = datetime.utcnow()

  # Calculate start time based on the interval
  if interval.lower() == 'minutes':
    start_time = current_time - timedelta(minutes=amount)
  elif interval.lower() == 'hours':
    start_time = current_time - timedelta(hours=amount)
  elif interval.lower() == 'days':
    start_time = current_time - timedelta(days=amount)
  else:
    raise HTTPException(
        status_code=400,
        detail=
        "Invalid interval. Allowed intervals are 'minutes', 'hours', or 'days'."
    )

  # Fetch data from MongoDB
  cursor = temperature_collection.find({
      "timestamp": {
          "$gte": start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
      }
  }).sort("timestamp", -1)
  items = [doc async for doc in cursor]
  return JSONResponse(content=json_util.dumps(items))


@app.get("/temperature/aggregated", tags=["GET endpoints"])
async def get_aggregated_data(start_date: str, end_date: str,
                              aggregation_type: str):
  try:
    # Convert start_date and end_date to datetime objects
    start = datetime.strptime(
        start_date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')
    end = datetime.strptime(end_date,
                            '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S.%f')

    # MongoDB aggregation pipeline
    pipeline = [{
        "$match": {
            "timestamp": {
                "$gte": start,
                "$lte": end
            }
        }
    }, {
        "$group": {
            "_id": None,
            "average_temp": {
                "$avg": "$temperature"
            },
            "max_temp": {
                "$max": "$temperature"
            },
            "min_temp": {
                "$min": "$temperature"
            }
        }
    }]

    # Execute the aggregation query asynchronously
    cursor = temperature_collection.aggregate(pipeline)
    aggregated_data = [doc async for doc in cursor]

    if not aggregated_data:
      raise HTTPException(
          status_code=500,
          detail=
          "Internal server error or wrong datetime format. Allowed format: YYYY-MM-DD HH:MM"
      )

  # Format and return the response based on the aggregation type
    data = aggregated_data[0]
    if aggregation_type == "average":
      return {"average_temperature": data['average_temp']}
    elif aggregation_type == "max":
      return {"maximum_temperature": data['max_temp']}
    elif aggregation_type == "min":
      return {"minimum_temperature": data['min_temp']}
    else:
      raise HTTPException(
          status_code=400,
          detail=
          "Invalid aggregation type, aggregation types: max, min, average")

  except ValueError as e:
    raise HTTPException(
        status_code=400,
        detail=f"Invalid datetime format: {e} or invalid aggregation type"
    ) from e

  except Exception as e:
    raise HTTPException(status_code=500,
                        detail=f"Invalid datetime format for: {e}") from e


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
