# Food Recognition AI (Python Backend)

This is the Python Flask backend for the Food Recognition AI application. It handles image processing, food detection using YOLO, and recipe generation using Google's Gemini LLM.

For full project details, setup, and end-to-end testing instructions, please see the [main README.md](../README.md) at the root of the project.

## Key Components
- `app.py`: The main Flask application file containing all API endpoints and logic.
- `requirements.txt`: Lists all Python dependencies.
- `api_test_guide.md`: Provides details on the API endpoint (`/predict`) and how to test it manually (e.g., with `curl`).

## Setup and Running
Refer to the "Manual End-to-End Testing" section in the [main README.md](../README.md) for detailed instructions on:
- Setting up a Python virtual environment.
- Installing dependencies from `requirements.txt`.
- Setting the crucial `GOOGLE_API_KEY` environment variable.
- Running the Flask development server.

## API
The primary API endpoint is `/predict`. See `api_test_guide.md` for more information.
