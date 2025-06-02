# Food Recognition AI with Recipes

This project implements a web application that uses YOLO for food item recognition from an uploaded image and then fetches a recipe and cooking instructions for the detected food item using a Large Language Model (LLM).

The application consists of a Python Flask backend and a Vue.js (Vite) frontend.

## Project Structure
```
/
├── backend/             # Python Flask backend
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies
│   ├── uploads/         # Temporary folder for image uploads (created automatically)
│   └── api_test_guide.md # Guide for testing the backend API
├── frontend/            # Vue.js (Vite) frontend
│   ├── src/
│   │   ├── components/  # Vue components (ImageUploader, ResultsDisplay)
│   │   ├── App.vue      # Main Vue application component
│   │   ├── main.js      # Vue application entry point
│   │   └── style.css    # Basic global styles
│   ├── public/          # Static assets for frontend
│   ├── index.html       # Main HTML file for frontend
│   ├── package.json     # Frontend dependencies and scripts
│   └── vite.config.js   # Vite configuration
└── README.md            # This file
```

## Features
- Image upload for food recognition.
- Food item identification using YOLOv8.
- Recipe and cooking instruction generation using Google's Gemini Pro LLM.
- User-friendly web interface built with Vue.js.

## Styling Notes
Styling is primarily handled within individual Vue components (`App.vue`, `ImageUploader.vue`, `ResultsDisplay.vue`) using `<style>` tags (some scoped, some global in App.vue). A global `frontend/src/style.css` also exists for very basic body styles.
The UI is designed to be clean, responsive, and provide clear feedback for loading and error states.

## Manual End-to-End Testing

Due to the complexity of the stack (Python/Flask, Node.js/Vue, AI models, API keys), automated end-to-end testing is not set up in this environment. Here’s how to test manually:

### 1. Backend Setup & Run
   a. **Navigate to the backend directory:**
      `cd backend`
   b. **Create and activate a Python virtual environment:**
      `python3 -m venv .venv`
      `source .venv/bin/activate` (On Windows: `.venv\Scripts\activate`)
   c. **Install Python dependencies:**
      `pip install -r requirements.txt`
      *(This may take some time as it includes PyTorch for YOLO.)*
   d. **Set the Google API Key:**
      You need a Google API key for the Gemini LLM. Set it as an environment variable:
      `export GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY_HERE'` (On Windows: `set GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE`)
   e. **Run the Flask application:**
      `python app.py`
   f. The backend server should now be running, typically on `http://localhost:5000`.

### 2. Frontend Setup & Run
   a. **Navigate to the frontend directory (in a new terminal):**
      `cd frontend`
   b. **Install Node.js dependencies:**
      `npm install`
   c. **Run the Vue development server:**
      `npm run dev`
   d. The frontend development server should now be running, typically on `http://localhost:5173` (Vite often uses port 5173 by default if 3000 is taken).

### 3. Perform Tests in Browser
   a. Open your web browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
   b. **Test Case 1: Successful Food Recognition**
      - Upload an image of a common food item (e.g., pizza, apple, banana).
      - Click "Recognize Food".
      - **Expected:** Loading indicator appears, then the detected food name, a recipe, and cooking instructions are displayed.
   c. **Test Case 2: Non-Food Image**
      - Upload an image that is clearly not food (e.g., a car, a landscape).
      - Click "Recognize Food".
      - **Expected:** A message indicating that no food item was detected or that recipe details could not be retrieved.
   d. **Test Case 3: No File Selected**
      - Click "Recognize Food" without selecting an image.
      - **Expected:** An error message like "Please select an image file first" should appear.
   e. **Test Case 4: Invalid File Type (if applicable)**
      - Try uploading a non-image file (e.g., a .txt file) if the file input doesn't strictly filter it.
      - **Expected:** The backend should ideally reject it, or the frontend might show an error if it attempts to process an invalid file.
   f. **Observe:**
      - Loading states during processing.
      - Error messages for backend issues (e.g., if the GOOGLE_API_KEY is invalid or missing, the recipe/instructions part should show an error).
      - Console logs in both backend and frontend terminals for any errors or diagnostic messages.

## Configuration Notes

### Backend API Key
- As mentioned in the setup, the `GOOGLE_API_KEY` environment variable **must** be set for the backend to fetch recipes. See the backend setup guide.

### Frontend API Endpoint
- The frontend component `frontend/src/components/ImageUploader.vue` currently has the backend API URL hardcoded as `http://localhost:5000/predict`.
- For deployment or if your backend runs on a different URL, this will need to be updated. Consider making this configurable via an environment variable for the frontend build process in a production setup.
