# 🗎 Documentation & Project Description 💼
This was a project for an assignment called: **portfolio project** in the course: ***IoT och molntjänster*** at https://nackademin.se/utbildningar/mjukvaruutvecklare/

Docs & API testing visit: https://arduino-temp-api.replit.app/docs

Author: Marcus Peterson

## 🗎 Name of project: ThermoLinkAi 🤖

<div align="center">
    <img src="images/thermolink_ai_logo.png" width="480">
</div>


## Introduction 📖
#### The idea for this project came about during the advent of OpenAi's release of the so called GPTs: https://openai.com/blog/introducing-gpts

<picture>
    <img src = "images/arduino-temp-project.png">
</picture>

##### 1.1. The Arduino detects temperatures using the DS18b20 digital Tempereture Probe sensor
##### 1.2 depending on temperature values, either one of the three LED's will blink RED=High temperature, BLUE=Low temperature & GREEN=Stable tempereture (Note this categories are arbitrary and are subject to change depending on target application and use cases)
##### 1.3 The Arduino communicates with a python script through "serial communication" *(You may wonder why the Arduino r4 use serial com instead of communicating through HTTPs or MQTT, that question gets answered in the Arduino Rev 4 & IoT section)*
#
##### 2.1 The python serial communicator not only handles serial com, but it also handles the POST request to the arduino temp API. It sends the temperature data, timestamp, which LED was blinking and finally which category of temperatures it belongs to
##### 2.2 That data gets sent to the https://arduino-temp-api.replit.app/insert_data endpoint
#
##### 3.1 The Arduino temp API handles the insertion of the data to a MongoDB hosted on Azure *(Note, there is no schema validation present due to scalability issues or the fact that the manager of this project doesn't want to refactor code that already works, as of date 2023-11-26. There will be another Arduino system integrated to this project that will be place outdoors in the near future*)
##### 3.2 Whenever there is a request to one of the available endpoints. The API makes a database operation on the Azure Cosmos DB
#
##### 4.1 ChatGPT (Specifically the ArduinoTempGPT) can only make GET requests
##### 4.2 Once ChatGPT has requested data through one of the GET endpoints the users requested data gets displayed in the chat




##
#### GPT's have a slightly different use case than to just simply be a ChatGPT with custom instructions. What differs GPT's from the previous implementations is the fact that we now can add ***actions*** to it (and custom data, which is less interesting). 
#### This means we can connect the GPT's to more than just 3 API's (The max number of plug-ins avaiable in a concurrent chat is 3). And as of date (2023-11-26) there is no indication that this is limited to only external API:s that you yourself have built (As far as the available information shows you only need to provide a OpenAPI schema and a privacy policy link in the actions tab when you're building your GPT). <img src = "images/build_gpt_instructions.png">
#### The Auth is only needed for the API's that have token-access only implemented
 
#### So if you have a favorite API that you want chatGPT to use, you don't need to host your own service that connects to this API and then this service in turn is connected to ChatGPT
#### NOTE: This presumes that you have access to said API either through a access token or other credentials (If the API doesn't require an access token, you can ignore this note). 
#### If you don't know how to write an OpenAPI schema you can check the: "schema.yaml" file in this repo to see how it is structured

#### Since GPT's are capable of using the "advanced data analysis" tool avaiable to it. We can make API calls, receive the data and make various calculations on it right inside if the ChatGPT interface.

### Here is a snippet example how that could look like:
<picture>
    <img src = "images/arduinogpt_sample.png">
</picture>

#### As you would sometimes expect from general purpose LLM's, the graph is a bit "wonky". But with a good prompt we could in theory acheive better results *(The recommendation is using fine-tuned open source models for this. Specifically tuned for this use case)*
#
#
# Arduino Rev 4 & IoT 📟
<picture>
    <img src = "images/ABX00087_01.ISO-LARGE.png" style="width:480px;">
</picture>

#### For this project the Arduino Rev 4 with a built in ESP-32 WiFi chip was used. This is a great choice if the project requires rapid deployment of a wireless prototype IoT-system. Since the Rev 4 is shipped together with the WiFis3 library. 

## Challenges
#### Even though the Rev 4 is an easy to use circuit that doesn't mean it doesn't come with some issues:

<ul>
<li>
    <h3>Register naming issues</h3>
</li>
<p> During the initial development of the Arduino code, the WiFiNINA library was used <img src = "images/wifi_img.png"></p>
<p>This is a great library when you want to build wireless systems, it has built in tooling for UDP and serverside functions. So if you want a ready to use toolkit and want a rapid protype use WiFiNINA</p>
<p>However, you have to keep in mind that the pinMode function expects certain register names: <img src = "images/nina_error.png">
<p>This seems to be a common issue with the library</p>
Since there wasn't a clear way of solving this (A possible issue might be that the Ardunio Rev 4 simply doesn't support the WiFiNINA library) after some extensive google searches and with the assistance if ChatGPT. 
<p>
</p>

<li><h3> <strong>The next library on the list was WiFiS3</strong></li> <img src = "images/s3_pic.png">
</h3>  This is the in-built WiFi library that comes with the Arduino Uno r4 core this, unfortunately also came with some issues since originally. The arduino was meant to speak directly to the API via the POST endpoint. But during the devlopment, problems arised with the fact that the HTTP/HTTPS doesn't work properly. This is most likely a HTTPS (Which the API uses) and not a HTTP problem. Since doing requests locally on a Flask test server is not an issue </p>
<li><h3> <strong>Using serial com is a skill issue </strong> </h3> </li>
<img src = "images/skill-issue-memes.gif">
<p>
As the meme would imply, using serial communication was the easiest solution to this, the downside is that Arduino r4 can now not function without the use of an external device such as a PC, another arduino, Raspberry Pi etc. We get a microcontroller with wireless functionality but we are not using it. The upside to this is that we can have better control over what gets sent to the the API thanks to the serial communicator interface. And make the neccessary changes as needed without having to manipulate our microcontroller to much. 

<img src = "images/python_code_snippet.png">


<h3>Video Demonstration</h3>
<video width="1080" height="720" controls>
  <source src="images/compressed_video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>



<p> As stated before, the tempereture categories are arbitrary, but for the indoor enviroment it was used in the tempereture categories are as follows</p>
<table>
    <tr>
    <th><h3>Category</h3></th>
    <th><h3>LED</h3></th>
    <th><h3>Ranges</h3></th>
    </tr>
    <tr>
    <th>Low (Låg)</th>
    <th>BLUE</th>
    <th><=14 °C</th>
    </tr>
    <tr>
    <th>High (Hög)</th>
    <th>RED</th>
    <th>>=40 °C</th>
    </tr>
    <tr>
    <th>Stable (stabil)</th>
    <th>GREEN</th>
    <th>>=15 °C and  <= 39 °C </th>
    </tr>
</table>
</p>
</p>
</ul>


<h3>Schematics</h3>
<img src = "images/schematics.png">
<img src = "images/arduino_real.png">

#
#

<div style="display: flex; align-items: center;">
  <h1 style="margin: 0; padding-right: 10px;">Arduino temp api</h1>
  <img src="images/fast_api_icon.png" alt="FastAPI icon" style="width: 50px; height: 50px;">
</div>
<img src = "images/my_api.png">

#### The entire API that the ArduinoTempGPT uses was built from the ground up using the FastAPI framework. Unlike Flask (which is often used in API devopment) which is general purpose framework for building microservices, small web apps and more. 

#### As the name implies, if you want rapid development and a production ready API your first choice should be FastAPI (If you are a python developer that is). By default, all of the function defintions can be constructed with asynchronicity in mind (The FastAPI decorators aren't by **default** async. But they inherently have support for it). 
#### If you want to test out the endpoints (using software such as postman) there is no neccessity in declaring any asynchronocity. But, by having the arduino temp API endpoints asynchronous. Third-party libraries (That use async), other applications and software that might utlize multi-threading and multi-processing to ensure the entire system runs without interruptions. (In theory) This will allow for faster executions of these libraries and systems. As it allows for multiple HTTP requests at the same time, and also if one endpoint fails. The entire system will not stop working. 

### POST endpoint
```cpp
https://arduino-temp-api.replit.app/temperature/insert_data
```
```bash
curl -X POST https://arduino-temp-api.replit.app/temperature/insert_data -H "arduino-temp-api: YOUR_API_KEY" -d "{\"temperature\": YOUR_TEMPERATURE_VALUE}"
```

```python
# FastAPI decorator & function

@app.post("/temperature/insert_data", tags=["POST endpoints"])
async def receive_temperature(request: Request, api_key: str = Security(get_api_key)):                              
```
#### This endpoint is the most important since it's the only way to insert data into the Azure Cosmos MongoDB. And it is the only endpoint that directly "manipulates" the database, a new API key can not be generated through any interfaces. Which means the Arduino r4 is the only device which is allowed and can insert new data into the database. Contact the author if you want to contribute with data to the MongoDB and get your own API-key.
#### 

### GET endpoints
```cpp
https://arduino-temp-api.replit.app/temperature/insert_data

https://arduino-temp-api.replit.app/temperature/fetch_data

https://arduino-temp-api.replit.app/temperature/by_category

https://arduino-temp-api.replit.app/temperature/time_interval

https://arduino-temp-api.replit.app/temperature/aggregated
```
#
#
```bash
curl -X 'GET' \
  'https://arduino-temp-api.replit.app/temperature/fetch_data?limit=10' \
  -H 'accept: application/json'

# By default limit = 10
```
```python
# FastAPI decorator & function
@app.get("/temperature/fetch_data", tags=["GET endpoints"])
async def get_items(limit: int = 10):
```
#
#
```bash
curl -X 'GET' \
  'https://arduino-temp-api.replit.app/temperature/by_category?category=SOME_CATEGORY' \
  -H 'accept: application/json'

# Allowed categories are: låg(low), stabil(stable), hög(high)
# Keep in mind the categories in the database are stored as the swedish words 
```
```python
# FastAPI decorator & function
@app.get("/temperature/by_category", tags=["GET endpoints"])
async def get_temperatures_by_category(category: str):
```
#
#
```bash
curl -X 'GET' \
  'https://arduino-temp-api.replit.app/temperature/time_interval?interval=SOME_INTERVAL&amount=10' \
  -H 'accept: application/json'

# Allowed intervals are: minutes, hours, days
# The amount can be: 1 to N (There is no limit)
```
```python
# FastAPI decorator & function
@app.get("/temperature/time_interval", tags=["GET endpoints"])
async def get_data_by_time_interval(interval: str, amount: int):
```
#
#
```bash
curl -X 'GET' \
  'https://arduino-temp-api.replit.app/temperature/aggregated?start_date=YYYY-MM-DD HH:MM&end_date=YYYY-MM-DD HH:MM&aggregation_type=average' \
  -H 'accept: application/json'

# The start date and end date must be: YYYY-MM-DD & HH:MM
# The allowed aggregation types are: average, max & min
```
```python
# FastAPI decorator & function
@app.get("/temperature/aggregated", tags=["GET endpoints"])
async def get_aggregated_data(start_date: str, end_date: str,
                              aggregation_type: str):
```
#
#
#### These endpoints are specifically designed to be used together with LLM's such as GPT-4 or other models finetuned for function calling
#### these endpoints can however be used outside of this context. 
### Deployment service:
<img src = "images/replit_logo.png">

### The reason Replit was used for the API deployment was for many reasons:
<ul>
    <li><h2>1: Dedicated IDE</h2></li>
    <h4> Since replit is both an online IDE & a deployment enviroment. Making and implementing new behaviors, functionality and more to a deployed software is extremely easy. Since there aren barely any steps to get an application up and running, all you have to do is: select the language environment, and that's it. You can start coding!  </h3>

<head>
    <title>Step-by-Step Guide</title>
    <style>
        .step {
            margin-bottom: 20px;
        }
        .step img {
            width: 100%;
            max-width: 500px; 
        }
        .step-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

<div class="step">
    <div class="step-header">Step 1</div>
    <img src="images/replit_1.png" alt="Step 1">
</div>

<div class="step">
    <div class="step-header">Step 2</div>
    <img src="images/replit_2.png" alt="Step 2">
</div>

<div class="step">
    <div class="step-header">Step 3</div>
    <img src="images/replit_3.png" alt="Step 3">
</div>

<div class="step">
    <div class="step-header">Step 4</div>
    <img src="images/replit_4.png" alt="Step 4">
</div>

<div class = "step">
    <div class = "step-header"> Deploy! </div>
    <img src = "images/replit_deploy.png" alt = "Deploy">
    <p> When you have deployed your project for the first time, the button will become the "redeploy" button</p>
    <p> Important to note: The run button allows for local testing & deployment</p>
</div>

</body>

<li><h2>2: Ease of use<h2></li>
<h4>With Replit also comes with an automatic packaging system, which means that, when you run your project for the first time Replit handles all of the neccessary pip installs for you (Note: This isn't consistent. Some packages you will have to pip install manually) </h4>
<img src = "images/poetry_image.png">

<li><h2>3: Easy deployment</h2></li>
<h4> Deployment on Replit is straightforward</h4>
<p>Unlike services such as heroku, Azure, AWS. In which you have to setup a workflow (arguably, this is the better solution. Since it allows for a more streamlined CI/CD). But due to the minimal proccessing power that was required for this API to function, I decided that Replit was the better choice. And first and foremost <p><bold>cheaper</bold></p>. Other than pressing the deploy button, it isnt much to it.</p>
</ul>
<br />

# Azure cosmos MongoDB 🛢
<img src =  "images/azure_image.png">
<h2>Setting up a database via Azure is an easy process (somewhat of a lie), and for this project a NoSQL schema was chosen</h2>
<p> Given the low complexity of the different types of data that is going to be stored in the database, no relational connections were neccessary for the data.</p>
<p> Out of all the resources that a user can create on Azure, the <p><bold>Azure Cosmos DB for MongoDB</bold></p> is the easiest one to set up, get it to run and connect to (In general MongoDB is a streamlined process, thanks to the staggering amount of learning resources given to us from both MongoDB themselves and tutorials available on the internet )</p>

```json
# Sample data from the database
{
	"_id" : ObjectId("655c59158e4b0dd680142d9d"),
	"temperature" : 29.59,
	"tempCategory" : "stabil",
	"ledColor" : "grön",
	"timestamp" : "2023-11-21 08:15:33.238475"
}
```
<p> The data itself is stored as a BSON object (Binary JSON) in a Mongo Database, like standard JSON it stores data in key:value pairs. Ands structurally it is similiar. With some key differences being that BSON encodes type and length information, which allows it to be traversed more quickly compared to JSON. Bson has some native-data types such as dates and binary data. This is core to how MongoDB stores data </p>


<div style="display: flex; align-items: center;">
  <h1 style="margin: 0; padding-right: 10px;">ChatGPT interface</h1>
  <img src="images/chatgpt_logo.png" alt="ChatGPT icon" style="width: 50px; height: 50px;">
</div>
<img src = "images/arduino_temp_image.png">
<p> Using a Large Language Model (GPT-4) as our intreface opens up many opportunities for different types of data exploration.</p>

<h2> Example below I have instructed ChatGPT to do a weather forecast using the scikit-learn library that is a part of it's python environement</h2>

<p>Unfortunately, due to the technological castrations and over-the-top safety guardrails that OpenAi have placed on GPT-4. Our prompts need to be a little "extreme" if we want it to do anything advanced (That is why it is once again advised to use a open-source LLM if you have the resources and capital instead of GPT-4)</p>

### Using the "Extreme Grandma Prompt"
**prompt: **
| | |
|:-------------------------:|:-------------------------:|
| ![First Image](images/chatgpt_prompt_1.png) | ![Second Image](images/chatgpt_demo_1.png) |
| ![Third Image](images/chatgpt_demo_2.png) | ![Fourth Image](images/chatgpt_demo_3.png) |




### Using a normal prompt

| | |
|:-------------------------:|:-------------------------:|
| ![First Image](images/normal_prompt_1.png) | ![Second Image](images/normal_prompt_2.png) |
| ![Third Image](images/normal_prompt_3.png) | ![Fourth Image](images/normal_prompt_4.png) |

If GPT-4 starts refusing to do as you are told, the advice is to simply start a new conversation, due to the fact that the context window is so high. Later down the conversation, GPT-4 might refuse to do seemingly mundane and none-controversial tasks. In the LLM space we call this the "refusing-circle-of-doom"



## However GPT-4 isn't an entirely useless piece of software

**prompt: "I want you to get temperature data (10 readings) and give me a stack chart using matplotlib. Remember to not forget A SINGLE TEMPERATURE READING in your code. Don't be lazy"**

| | |
|:-------------------------:|:-------------------------:|
| ![First Image](images/temp_chart_1.png) | ![Second Image](images/temp_chart_2.png) |
| ![Third Image](images/temp_chart_3.png) | ![Fourth Image](images/temp_chart_4.png) |



# Final thoughts & Conclusions
<p>The project was a fun experience, however there was certain realisations:</p>

<ul>
<li><p>During the development of this project, the realisation that the ArduinoTempGPT is only capable of doing "smaller" tasks came after the fact that the Arduino Temp API was finished.</p></li>
<li><p>More functionalities could have been added to the API such as a weather forecasting endpoint that that predicts the weather outside of the the ChatGPT interface</p></li>

<li><p>Better functionalities in how data is retrieved could be implemented. There are certain restrictions in how many json objects ArduinoTempGPT can retrieve, therefore it would have been much wise if the the API would return the json response as a file. This is a feature that might be added in the future</p></li>

<li><p> It would have to be fun and interesting to host a Open Source model in the cloud that is fintuned for function calling: <a href="https://huggingface.co/Trelis/Llama-2-7b-chat-hf-function-calling">Trelis/Llama-2-7b-chat-hf-function-calling</a>. However due to limitations in resources & limited capital this wasn't possible</p></li>

<li><p> Finnally, the last part that unfortunetaly didn't get implemented was websocket functionalites on our live API. Hosting a simple HTML page locally does work however. Feel free to test it using the vizualise_flask.py</p></li>
</ul>
