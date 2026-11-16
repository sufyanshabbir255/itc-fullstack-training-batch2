"""
Package marker for app.schemas.

"Schemas" are Pydantic models. They describe the SHAPE of data:
  - what the client must send in a request body
  - what the API promises to send back (used with `response_model`)
FastAPI also turns them into the "Schemas" section of the OpenAPI docs.
"""
