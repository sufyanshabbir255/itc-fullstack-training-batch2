How to run this app with Docker
You only need Docker installed. No Python, no venv, no code.

1. Make a .env file
   Create a file called .env in any empty folder with these two lines:

SECRET_KEY=paste-a-random-key-here
REFRESH_SECRET_KEY=paste-another-random-key-here
Make your own random keys (run this twice, use one result for each line):

docker run --rm python:3.13-slim python -c "import secrets; print(secrets.token_hex(32))"
Never share or commit your .env.

2. Run the app
   From the folder with your .env:

docker run --rm --env-file .env -p 8000:8000 dinhasnaad/fastapi-learning:v1 3. Open it
Go to http://localhost:8000/docs

Stop it with Ctrl + C.
