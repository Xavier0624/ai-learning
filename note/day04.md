## concept
stream request with `stream=True`: model will return a piece of response called chunk.

The web may be unstable, and API may be restricted. We need:
- Timeout
- Retry

```
client = OpenAI(
    timeout = 30,
    max_retries = 3,
    api_key = ...,
    base_url = ...
)
```

Token usage:
- A ordinary request can get usage with
  ```
  response.usage.prompt_tokens
  response.usage.total_tokens
  response.usage.completion_tokens
  ```
- The stream request doesn't return the usage parameter, but can solve it with `stream_usage={"include_usage": true}`
  
