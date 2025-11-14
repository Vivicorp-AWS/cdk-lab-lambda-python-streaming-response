import boto3
import asyncio
import httpx
import json

client = boto3.client('cloudformation')

stack = client.describe_stacks(
    StackName='cdklab-lambdastreaming-stack',
)
function_url = stack['Stacks'][0]['Outputs'][0]['OutputValue']

# Example 1
async def stream_lorem_ipsum_response():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', function_url) as response:
            async for chunk in response.aiter_text():
                print(chunk, end='', flush=True)

asyncio.run(stream_lorem_ipsum_response())

# Example 2
# async def stream_bedrock_hello_world_response():
#     async with httpx.AsyncClient() as client:
#         async with client.stream('GET', f"{function_url}bedrock/") as response:
#             # async for chunk in response.aiter_text():
#             #     print(chunk, end='', flush=True)
            
#             async for line in response.aiter_lines():
#                 print(line, flush=True)

# asyncio.run(stream_bedrock_hello_world_response())

# Example 3
# async def stream_bedrock_custom_promot_response():
#     async with httpx.AsyncClient() as client:
#         async with client.stream(
#             'POST',
#             f"{function_url}bedrock/",
#             data=json.dumps({'prompt': "Who are you? Please describe it specificly, tell me as more as you can. I'\''ve set your output token to 10000, tell me more!"})
#             ) as response:
#             # async for chunk in response.aiter_text():
#             #     print(chunk, end='', flush=True)
            
#             async for line in response.aiter_lines():
#                 print(line, flush=True)

# asyncio.run(stream_bedrock_custom_promot_response())