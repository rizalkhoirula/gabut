## API Endpoint: /predict
**Method:** POST
**Request:** Multipart form data with a 'file' field containing the image.

### Success Response (200 OK)
If a food item is detected and recipe is generated:
```json
{
  "food_name": "String (e.g., Pizza)",
  "yolo_message": "String (e.g., Detected Pizza with 0.87 confidence)",
  "recipe": "String (Ingredients list)",
  "instructions": "String (Cooking instructions)"
}
```

### Error Responses
**400 Bad Request (e.g., no file, wrong file type):**
```json
{
  "error": "String (description of the error)"
}
```
**404 Not Found (e.g., YOLO doesn't detect food):**
```json
{
  "error": "String (e.g., No food item detected...)",
  "food_name": null
}
```
**500 Internal Server Error (e.g., unexpected error during processing):**
```json
{
  "error": "String (description of the server error)"
}
```
**Note on LLM Errors:** If the LLM part fails (e.g., API key issue), the response might still be 200 OK but the 'recipe' and 'instructions' fields will contain error messages.

### Example `curl` command for testing:
Assumes the Flask server is running on `localhost:5000`, and you have an image named `food_image.jpg` in the current directory.
Replace `YOUR_GOOGLE_API_KEY` with your actual key if testing locally.
```bash
# Make sure to set the API key in your environment when running the Flask server:
# export GOOGLE_API_KEY='YOUR_GOOGLE_API_KEY'
# python app.py

curl -X POST -F "file=@food_image.jpg" http://localhost:5000/predict
```
