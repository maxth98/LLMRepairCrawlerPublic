# LLMRepairCrawler

## Description

This university project involves the creation of a geospatial question and answer system that combines LLM's (Large language models), langchains and a modern frontend. 
The frontend was built using React, Vite, and TailwindCSS. It incorporates a world map, provided by the Mapbox JS library, and a search bar interface where users can enter their queries. The results of these queries are highlighted in map in order to answer the user's questions.

The backend is where the data is collected, processed, and then used to answer user queries. It collects geospatial data from two sources: Google Maps and OpenStreetMaps (OSM), the latter accessed through the Overpass API. Data extraction from Google Maps is done using the Apify tool. Once the data is obtained, it is passed through Langchain, a library designed for developing applications with LLMs, to convert the raw data into an embedding that an LLM can interpret. This conversion process allows the LLM to use the information in a meaningful way, such as answering user queries. The embeddings are stored in ChromaDB, a specialized vector database. We have used OpenAI in our example, but the application can be extended to other LLMs, such as Alpaca or LLaMA.

Flask was used to create a REST API that provides a communication link between the frontend and the backend. When a user submits a query, it is sent through this API to the backend for processing. The LLM then provides a response based on the data embeddings, which is returned to the user on the frontend.

In the frontend React was used with TailwindCSS to display the results on the map. The technology we used for displaying the map was Mapbox. For every entry inside our dataset a marker is displayed on the map, depending on whether we are utilizing Google Maps or OpenStreetMaps, there will be different amount of information available. On every marker the user can click and the popup of the corresponding marker opens, displaying the details. If the user queries something like "Fahrradreparatur in Graz", the resulting markers will be highlighted on the map with an orange color. If there are no result, no marker will be highlighted and an error message will be displayed.

To run this project, you will need to provide Mapbox, Apify, and OpenAI API keys in the tokens.json file using the following format:

{
  "mapbox": "MAPBOX SECRET KEY",
  "mapbox_pb": "MAPBOX PUBLIC KEY",
  "apify_id": "APIFY ID",
  "apify_token": "APIFY TOKEN",
  "openai": "OPEN AI API KEY"
}

and this frontend was tested on node version: 18.5

## Backend

### Installation

Install Python ``>= 3.9`` and  Poetry: ``https://python-poetry.org/docs/``

Run ``poetry install`` from Backend folder

Usage: ``poetry run python backend.py [port] [debug] [log]``

Example: ``poetry run python backend.py 5000 True data/Log.log``

Run ``site-crawler.py`` to annotate website conent to the apify_result.json dataset

### Example API call

#### Apify

Retrieve dataset: http://localhost:5000/dataset?dataset_id=QMWb9nD2dY5qYvfIk&source=apify

Retrieve answer: http://localhost:5000/answer?question=Fahrradreparatur%20in%20Graz&dataset_id=QMWb9nD2dY5qYvfIk&source=apify

#### OSM

Retrieve dataset: http://localhost:5000/dataset?dataset_id=styria_proc&source=osm

Retrieve answer: http://localhost:5000/answer?question=Fahrradreparatur%20in%20Graz&dataset_id=styria_proc&source=osm

## Frontend

### Installation

Install vite ``npm i vite``

Run ``npm install`` inside the root of the frontend folder to install all packages

Run ``npm run dev`` to start the local development server in the frontend

It will be running on ``localhost:5173``


P.S.: If you develop in VS Code install Tailwindcss extension: [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)

