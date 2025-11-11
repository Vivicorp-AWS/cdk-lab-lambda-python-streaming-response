#!/bin/bash

# [NOTE]
# 1. Add '/opt/python/' to PYTHONPATH to use klayer lambda layer's package
# 2. Add `/opt/python/lib/python3.12/site-packages` to PYTHONPATH
# to use the layer built with Git Repo: aws-samples/aws-lambda-layer-builder
# [NOTE] To find the right PYTHONPATH, call `ls /opt/` here
# with many trail-and-error` to get the real path!

PATH=$PATH:$LAMBDA_TASK_ROOT/bin \
    PYTHONPATH=$PYTHONPATH:/opt/python/:/opt/python/lib/python3.12/site-packages/:$LAMBDA_RUNTIME_DIR \
    exec python -m uvicorn --port=$PORT main:app

# [USAGE]
# 1. with curl
# curl -N <FUNCTION_URL>
# 
# 2. with Python Requests
# import requests

# r = requests.get('<FUNCTION_URL>', stream=True)

# # Option 2.1: iter_lines()
# for line in r.iter_lines():
#     if line:
#         decoded_line = line.decode('utf-8')
#         print(decoded_line)

# # Option 2.2: iter_content()
# for chunk in r.iter_content():
#     if chunk:
#         decoded_chunk = chunk.decode('utf-8')
#         print(decoded_chunk, end="")

# # Verify if the response is stream
# # by looking for "Transfer-Encoding" header
# assert r.headers['Transfer-Encoding'] == 'chunked'