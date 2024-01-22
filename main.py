from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import cv2
import pytesseract
from io import BytesIO
import numpy as np

app = FastAPI()

# Set the path to the Tesseract executable (if not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ExtractedTextResponse(BaseModel):
    text: str


@app.get('/')
async def home():
  return {"name": "Junius"}

@app.post("/ocr-image")
async def create_upload_file(file: UploadFile):
    # Ensure the uploaded file is an image
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read the image using OpenCV
    contents = await file.read()

    # Convert the bytes to a NumPy array
    np_array = np.frombuffer(contents, np.uint8)

    # Decode the image
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray_image)

    # Create a response object
    response = ExtractedTextResponse(text=text)

    return JSONResponse(content=response.dict())