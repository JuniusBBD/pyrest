from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import easyocr
from PIL import Image
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(['en'])

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        result = reader.readtext(image)

        extracted_text = ""
        for detection in result:
            extracted_text += detection[1] + "\n"

        return JSONResponse(content={"extracted_text": extracted_text}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
