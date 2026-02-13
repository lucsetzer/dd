from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/analyze/github")
async def github_analyzer(request: Request):
    return templates.TemplateResponse("github_analyzer.html", {
        "request": request,
        "title": "Analyze GitHub Repository"
    })

@router.get("/analyze/api")
async def api_analyzer(request: Request):
    return templates.TemplateResponse("api_analyzer.html", {
        "request": request,
        "title": "Analyze API Documentation"
    })

@router.get("/analyze/snippet")
async def snippet_analyzer(request: Request):
    return templates.TemplateResponse("snippet_analyzer.html", {
        "request": request,
        "title": "Analyze Code Snippet"
    })

@router.get("/analyze/security")
async def security_analyzer(request: Request):
    return templates.TemplateResponse("security_analyzer.html", {
        "request": request,
        "title": "Security Scan"
    })

