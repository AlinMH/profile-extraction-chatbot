# Profile Extraction Chatbot

## Requirements
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Gemini AI API key

## Installation Steps
Install the application dependencies using uv
```bash
uv sync
```

## Run application locally

- Set the environment variable `GEMINI_API_KEY` with your Gemini AI API key
```bash
export GEMINI_API_KEY=<your_gemini_api_key>
```
Run the webserver using the following command
```bash
uv run uvicorn profile_extraction_chatbot.main:app --host=0.0.0.0 --port=5000 --reload
```
Open the browser and navigate to http://localhost:5000/ and start chatting with the Chatbot


## Run application using Docker
Build the docker image using the following command

```bash
docker build -t profile_extraction_chatbot .
```
Run the docker container using the following command

```bash
docker run -p 5000:5000 -e GEMINI_API_KEY=<your_gemini_api_key> profile_extraction_chatbot
```

Open the browser and navigate to http://localhost:5000/ and start chatting with the Chatbot
