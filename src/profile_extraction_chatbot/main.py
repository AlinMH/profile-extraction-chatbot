from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from pydantic_ai import Agent

from . import constants, schemas

app = FastAPI()

agent = Agent(
    "gemini-1.5-flash",
    result_type=schemas.ResponseToUser,
    system_prompt=constants.SYSTEM_PROMPT,
    retries=5,
)


THIS_DIR = Path(__file__).parent
STATIC_FILES_DIR = THIS_DIR.parent / "static"


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse((STATIC_FILES_DIR / "index.html").read_bytes())


@app.websocket("/ws")
async def chatbot_websocket(websocket: WebSocket):
    await websocket.accept()

    # Send welcome message to the user.
    await websocket.send_text(constants.WELCOME_MESSAGE)

    current_user_profile = schemas.UserProfile.empty_instance()
    current_score = 0
    message_history = []
    async for data in websocket.iter_text():
        if data == constants.END_SIGNAL:
            # Send a summary of the user profile and end the conversation.
            result = await agent.run(
                user_prompt=constants.PROFILE_SUMMARY_PROMPT,
                message_history=message_history,
            )
            await websocket.send_text(f"{result.data.message}")
            await websocket.close()
            break

        result = await agent.run(user_prompt=data, message_history=message_history)
        message_history.extend(result.new_messages())

        current_score = result.data.user_profile.compute_completeness_score()
        current_user_profile = result.data.user_profile
        await websocket.send_text(
            f"{result.data.message}\n"
            f"Profile completeness score: {current_score}\n{current_user_profile}"
        )
