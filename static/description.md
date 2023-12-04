# A temperature monitoring and control API

This is a temperature monitoring and control API that offers a comprehensive set of endpoints for managing temperature data and controlling temperature-related devices. Utilizing data from the Arduino Uno Rev4, this API provides real-time monitoring, data insertion, retrieval, query, and aggregation functionalities.
The main purpose of the API is to be the backend layer for the custom made ChatGPT called: ArduinoTempGPT

## Features
- **Real-time Data Insertion**: The API allows Arduino Uno Rev4 to insert temperature data in real-time along with the associated timestamp.

- **Data Retrieval**: Users can retrieve a specified number of recently added temperature data entries. The API supports fetching data based on time intervals and temperature categories.

- **Temperature Querying**: The API provides endpoints for temperature data querying, enabling users to retrieve data for specific temperature categories and time intervals.

- **Aggregated Data**: The API offers aggregation capabilities to calculate average, maximum, and minimum temperatures within a specified time range.


## Endpoints
1. `/temperature/insert_data`: Endpoint for real-time insertion of temperature data from a Arduino Uno Rev4.
2. `/temperature/fetch_data`: Fetch a specified number of temperature data entries.
3. `/temperature/by_category`: Fetch temperature data based on specific temperature categories.
4. `/temperature/time_interval`: Fetch temperature data within a specific time interval.
5. `/temperature/aggregated`: Fetch aggregated temperature data within a specified time range.


## Data Processing
The API processes temperature data received from the Arduino Uno Rev4 and provides insights into temperature trends, anomalies, and aggregated statistics. This allows for efficient analysis and monitoring of temperature-related activities.

## Data Source
The API sources temperature data from the Arduino Uno Rev4 which is stored in a Azure Cosmos Mongodb database, ensuring accurate and reliable data. The Arduino Uno Rev4 serves as a foundational component for data collection and temperature monitoring.

In summary, the Temperature Monitoring and Control API, utilizing data from the Arduino Uno Rev4, offers robust functionality for comprehensive temperature management, control, and monitoring.

## ArduinoTempGPT
The ArduinoTempGPT can collect various types of data from the endpoints, with the capabilities of ChatGPT and it's integrated tooling do caluclations, plotting on a graph and much more. You can vizualise data in ways that we didn't think about before. 

If you want to test it out for yourself: 
<a href=https://chat.openai.com/g/g-336zTZaUr-arduinotempgpt> 
https://chat.openai.com/g/g-336zTZaUr-arduinotempgpt
</a>

### Author: Marcus Peterson
#### Visit my github: 
<a href=https://github.com/Marcus-Peterson>
https://github.com/Marcus-Peterson
</a>