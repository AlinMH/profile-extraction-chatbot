from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from pydantic_ai import Agent

from profile_extraction_chatbot import constants
from profile_extraction_chatbot.schemas import UserProfile

app = FastAPI()
ResultType = Union[UserProfile, str]

agent: Agent[None, ResultType] = Agent(
    "gemini-1.5-flash",
    result_type=ResultType,
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

    current_user_profile = UserProfile.empty_instance()
    current_score = 0
    message_history = []
    async for data in websocket.iter_text():
        if data == constants.END_SIGNAL:
            # Send a summary of the user profile and end the conversation.
            result = await agent.run(
                user_prompt=constants.PROFILE_SUMMARY_PROMPT,
                message_history=message_history,
            )
            await websocket.send_text(f"{result.data}")
            await websocket.close()
            break

        result = await agent.run(user_prompt=data, message_history=message_history)
        message_history.extend(result.new_messages())

        if isinstance(result.data, UserProfile):
            current_score = result.data.compute_completeness_score()
            current_user_profile = result.data
            await websocket.send_text(
                f"Profile completeness score: {current_score}\n{current_user_profile}"
            )
        else:
            await websocket.send_text(
                f"{result.data} \nProfile completeness score: {current_score}\n{current_user_profile}"
            )
