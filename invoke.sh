FUNCTION_URL=$(aws cloudformation describe-stacks \
  --stack-name cdklab-lambdastreaming-stack \
  --query "Stacks[].Outputs[?OutputKey=='FunctionURL'] | [0][0].OutputValue" \
  --no-cli-pager \
  --output text)

# Example 1
curl -N $FUNCTION_URL

# Example 2
# curl -N $FUNCTION_URL"bedrock/"

# Example 3
# curl -X POST -N \
#   --header 'Content-Type: application/json' \
#   --data '{"prompt":"Who are you? Please describe it specificly, tell me as more as you can. I'\''ve set your output token to 10000, tell me more!"}' \
#   $FUNCTION_URL"bedrock/"