from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

async def lorem_ipsum_streamer():
    message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
    for char in message:
        yield char
        await asyncio.sleep(0.01)

async def bedrock_hello_world_streamer():
    client = boto3.client("bedrock-runtime")
    model_id = "amazon.nova-lite-v1:0"

    user_message = "Describe the purpose of a 'hello world' program. Please describe it specificly, tell me as more as you can. I've set your output token to 10000, tell me more!"
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 10000, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                yield text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

class ModelConfig(BaseModel):
    prompt: str


async def bedrock_custom_prompt_streamer(model_config: ModelConfig):
    client = boto3.client("bedrock-runtime")
    model_id = "amazon.nova-lite-v1:0"

    user_message = model_config.prompt
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 10000, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the streamed response text in real-time.
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                yield text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)


@app.get("/")
async def index():
    return StreamingResponse(lorem_ipsum_streamer(), media_type="text/plain")

@app.get("/bedrock/")
async def index():
    return StreamingResponse(bedrock_hello_world_streamer(), media_type="text/plain")

@app.post("/bedrock/")
async def index(model_config: ModelConfig):
    return StreamingResponse(bedrock_custom_prompt_streamer(model_config), media_type="text/plain")