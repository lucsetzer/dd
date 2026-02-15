from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@router.get("/github-simple")
async def github_form(request: Request):
    return templates.TemplateResponse("github_analyzer.html", {"request": request})

@router.post("/github-simple")
async def github_analyze(
    request: Request,
    repo_url: str = Form(...),
    branch: str = Form("main"),
    level: str = Form("professional")
):
    """Simple version - NO queue, NO loading page, NO background tasks"""
    
    try:
        # Call AI directly (this waits)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "You analyze GitHub repositories."},
                        {"role": "user", "content": f"Analyze this repo: {repo_url}"}
                    ]
                },
                timeout=60.0
            )
            result = response.json()
            ai_text = result["choices"][0]["message"]["content"]
        
        # Show results directly
        return templates.TemplateResponse("result.html", {
            "request": request,
            "result": ai_text,
            "repo_url": repo_url
        })
        
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })