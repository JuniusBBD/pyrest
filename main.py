from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import easyocr
import io
import tempfile
import os

app = FastAPI()

# Define EasyOCR reader
reader = easyocr.Reader(['en'])

class ExtractedTextResponse:
    def __init__(self, text):
        self.text = text

@app.post("/extract_text")
async def extract_text_from_image(file: UploadFile = File(...)):
    # Ensure the uploaded file is an image
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Create a temporary file to save the uploaded image
    with tempfile.NamedTemporaryFile(delete=False) as temp_image:
        temp_image.write(await file.read())
        temp_image_path = temp_image.name

    try:
        # Read the image using EasyOCR by providing the file path
        result = reader.readtext(temp_image_path)

        # Extract text from the EasyOCR result
        extracted_text = ' '.join([text[1] for text in result])

        # Create a response object
        response = ExtractedTextResponse(text=extracted_text)

        return JSONResponse(content=response.__dict__)

    finally:
        # Cleanup: Delete the temporary file
        os.remove(temp_image_path)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=1000)
