<secrets>
The following secrets and variables for accessing external services have been set in environment variables:

- Service: OpenAI
  Variables: `OPENAI_API_KEY` 
  Description: Used to access OpenAI and third-party LLMs via OpenAI-compatible API (supported models: `gpt-4.1-mini`, `gpt-4.1-nano`, `gemini-2.5-flash`). Install with `pip3 install openai` and use `client = OpenAI()` directly (API key and base URL pre-configured); to use original OpenAI API, manually override `base_url=\'https://api.openai.com/v1\'`. 
</secrets>
