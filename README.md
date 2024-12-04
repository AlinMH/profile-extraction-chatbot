# Installation

## Requirements
- Python 3.12 or higher
- [poetry](https://python-poetry.org/docs/#installation)
- Gemini AI API key

## Steps
- Install the application dependencies using poetry
```bash
poetry install
```

- Set the environment variable `GEMINI_API_KEY` with your Gemini AI API key
```bash
export GEMINI_API_KEY=<your_gemini_api_key>
```

- Run the webserver using the following command
```bash
uvicorn profile_extraction_chatbot.main:app --host=0.0.0.0 --port=5000 --reload
```
- Open the browser and navigate to `http://localhost:5000/` and start chatting with the Chatbot
