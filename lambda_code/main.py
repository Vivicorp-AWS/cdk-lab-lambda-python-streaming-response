from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

# async def streamer():
#     message = "This is streaming from Lambda!\n"
#     for char in message:
#         yield char
#         await asyncio.sleep(0.5)

async def streamer():
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime")

    # Set the model ID, e.g., Amazon Nova Lite.
    model_id = "amazon.nova-lite-v1:0"

    # Start a conversation with the user message.
    user_message = "Describe the purpose of a 'hello world' program in one line. Please describe it specificly, tell me as more as you can. I've set your output token to 10000, tell me more!"
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
    return StreamingResponse(streamer(), media_type="text/html")
