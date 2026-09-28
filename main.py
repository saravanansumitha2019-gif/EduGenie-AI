import os 
from pathlib import Path 
 
from dotenv import load_dotenv 
from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse, JSONResponse 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 
from pydantic import BaseModel, Field 
 
from qna import answer_question 
from explanation_module import explain_topic 
from quiz_module import generate_quiz 
from summary_module import summarize_text 
from learning_path import get_learning_recommendations 
from gemini_client import GeminiGenerationError
 
 
load_dotenv() 
 
BASE_DIR = Path(__file__).resolve().parent 
 
app = FastAPI( 
    title="EduGenie", 
    description="Google Gemini Powered Learning Assistant", 
    version="1.0.0" 
) 


@app.exception_handler(GeminiGenerationError)
async def handle_gemini_error(request: Request, error: GeminiGenerationError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(error)},
    )
 
app.mount( 
    "/static", 
    StaticFiles(directory=BASE_DIR / "static"), 
    name="static" 
) 
 
templates = Jinja2Templates( 
    directory=str(BASE_DIR / "templates") 
) 
 
 
# ----------------------------- 
# Request Models 
# ----------------------------- 
 
class TextRequest(BaseModel): 
    text: str = Field( 
        ..., 
        min_length=1, 
        max_length=30000 
    ) 
 
 
class QARequest(BaseModel): 
    question: str = Field( 
        ..., 
        min_length=1, 
        max_length=10000 
    ) 
 
 
class QuizRequest(BaseModel): 
    text: str = Field( 
        ..., 
        min_length=1, 
        max_length=30000 
    ) 
 
 
class LearningPathRequest(BaseModel): 
    topic: str = Field( 
        ..., 
        min_length=1, 
        max_length=500 
    ) 
 
 
# ----------------------------- 
# Frontend 
# ----------------------------- 
 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
 
# ----------------------------- 
# Health Check 
# ----------------------------- 
 
@app.get("/health") 
async def health(): 
 
    return { 
        "status": "ok", 
        "gemini_configured": bool( 
            os.getenv("GEMINI_API_KEY") 
        ) 
    } 
 
 
# ----------------------------- 
# Q&A 
# ----------------------------- 
 
@app.post("/qa") 
async def qa(payload: QARequest): 
 
    result = answer_question( 
        payload.question 
    ) 
 
    return { 
        "result": result 
    } 
 
 
# ----------------------------- 
# Explanation 
# ----------------------------- 
 
@app.post("/explain") 
async def explain(payload: TextRequest): 
 
    result = explain_topic( 
        payload.text 
    ) 
 
    return { 
        "result": result 
    } 
 
 
# ----------------------------- 
# Quiz 
# ----------------------------- 
 
@app.post("/quiz") 
async def quiz(payload: QuizRequest): 
 
    return generate_quiz( 
        payload.text 
    ) 
 
 
# ----------------------------- 
# Summarization 
# ----------------------------- 
 
@app.post("/summarize") 
async def summarize(payload: TextRequest): 
 
    result = summarize_text( 
        payload.text 
    ) 
 
    return { 
        "result": result 
    } 
 
 
# ----------------------------- 
# Learning Path 
# ----------------------------- 
 
@app.post("/learn/recommendations") 
async def recommendations( 
    payload: LearningPathRequest 
): 
 
    result = get_learning_recommendations( 
        payload.topic 
    ) 
 
    return { 
        "result": result 
    }