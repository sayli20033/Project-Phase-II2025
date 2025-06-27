from fastapi import FastAPI
from pydantic import BaseModel
from app import analyze_code, guess_language

app = FastAPI()

class CodeInput(BaseModel):
    code_snippet: str
    language: str

@app.post("/analyze")
async def analyze_code_api(data: CodeInput):
    detected = guess_language(data.code_snippet)

    # Optional: Warn if mismatch
    if detected != data.language:
        return {"analysis": f"⚠ Language mismatch detected! Selected: {data.language}, but detected: {detected}. Please check."}

    result = analyze_code(data.code_snippet)
    return {"analysis": result}