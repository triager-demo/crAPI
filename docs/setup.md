# Configuration

Local Compose settings are in `deploy/docker/.env`. Keep the default loopback bind for local use.

## Chatbot LLM configuration

The chatbot supports multiple LLM providers. Provider selection and models are set via environment variables. OpenAI and Anthropic keys are set via the API (with env fallback); all other providers use env credentials only.

Core settings:
- `CHATBOT_LLM_PROVIDER`: `openai`, `anthropic`, `azure_openai`, `bedrock`, `vertex`, `groq`, `mistral`, `cohere`
- `CHATBOT_LLM_MODEL`: optional, provider model name. Defaults per provider:
  - openai: `gpt-4o-mini`
  - anthropic: `claude-sonnet-4-20250514`
  - bedrock: `anthropic.claude-3-sonnet-20240229-v1:0`
  - vertex: `gemini-1.5-flash`
  - groq: `llama-3.3-70b-versatile`
  - mistral: `mistral-large-latest`
  - cohere: `command-r-plus`
  - azure_openai: uses `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `CHATBOT_EMBEDDINGS_MODEL`: optional embeddings model name (used across providers)
- `CHATBOT_EMBEDDINGS_DIMENSIONS`: optional, defaults to `1536`

OpenAI (API, optional env fallback):
- POST `/genai/init` with `{"openai_api_key":"..."}` (per-session)
- `CHATBOT_OPENAI_API_KEY` (optional env fallback)

Anthropic (API, optional env fallback):
- POST `/genai/init` with `{"anthropic_api_key":"..."}` (per-session)
- `ANTHROPIC_API_KEY` (optional env fallback)

Azure OpenAI (env only):
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT`
- Auth: `AZURE_OPENAI_API_KEY` or `AZURE_AD_TOKEN` (managed identity)
- Optional: `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT`

AWS Bedrock (env only):
- `AWS_REGION` and either:
  - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` (optional), or
  - `AWS_BEARER_TOKEN_BEDROCK`

Google Vertex AI (env only):
- `VERTEX_PROJECT`, `VERTEX_LOCATION`
- `GOOGLE_APPLICATION_CREDENTIALS` (optional if using ADC in GCP environments)

Groq / Mistral / Cohere (env only):
- `GROQ_API_KEY`, `MISTRAL_API_KEY`, `COHERE_API_KEY`
