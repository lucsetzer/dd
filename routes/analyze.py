from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from shared.utils import loading_response
from shared.queue import analysis_queue
from fastapi.responses import RedirectResponse
from routes.analyzers.base import run_analysis

print(f"⚙️ BACKGROUND - Queue ID: {id(analysis_queue)}")
print(f"⚙️ BACKGROUND - Queue has: {list(analysis_queue.keys())}")
print(f"🚀 MODULE IMPORT - Queue ID: {id(analysis_queue)}")
print(f"🚀 MODULE IMPORT - Queue empty? {len(analysis_queue)}")

import uuid
import asyncio
import time
import threading

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

@router.post("/process-api")
async def process_api(
    request: Request,  # Add this
    api_url: str = Form(...),
    api_type: str = Form("auto"),
    level: str = Form("professional"),
    specific_questions: str = Form("")
):
    """Fetch and analyze API documentation"""
    analysis_id = str(uuid.uuid4())
    
    # Use the SAME queue
    from shared.queue import analysis_queue  # Make sure this exists
    
    analysis_queue[analysis_id] = {
        "api_url": api_url,
        "api_type": api_type,
        "level": level,
        "specific_questions": specific_questions,
        "status": "processing",
        "progress": 0.1,
        "message": "Fetching API documentation...",
        "created_at": time.time()
    }
    print(f"📝 Just inserted {analysis_id}")
    print(f"📝 Queue now has: {list(analysis_queue.keys())}")
    print(f"📝 Length of queue: {len(analysis_queue)}")
    print(f"📝 POST ROUTE - Queue ID: {id(analysis_queue)}")
    print(f"📝 POST ROUTE - Queue has: {list(analysis_queue.keys())}")


    # Start background task - SAME PATTERN
    asyncio.create_task(analyze_api_background(analysis_id))
    
    # Use the SAME loading response function
    return await loading_response(analysis_id)

async def analyze_api_background(analysis_id: str):
    """Background task for API analysis"""
    from shared.queue import analysis_queue
    
    try:
        data = analysis_queue[analysis_id]
        
        # Update progress
        data["progress"] = 0.3
        data["message"] = "Fetching documentation..."
        
        # Simulate work (replace with real API fetching)
        await asyncio.sleep(2)
        
        data["progress"] = 0.6
        data["message"] = "Analyzing endpoints..."
        await asyncio.sleep(1)
        
        # Mock result
        result = f"""# API Documentation Analysis

**URL:** {data['api_url']}
**Type:** {data['api_type']}
**Level:** {data['level']}

## Overview
This API provides endpoints for data access.

## Key Endpoints
- GET / - Returns documentation
- POST /data - Submits data

## Authentication
API key required in headers.
"""
        
        data["result"] = result
        data["status"] = "complete"
        data["progress"] = 1.0
        
    except Exception as e:
        data["status"] = "error"
        data["error"] = str(e)
        print(f"❌ API analysis error: {e}")


async def process_api_background(analysis_id: str):
    """Background task for API analysis"""
    print(f"🚀 API background started for {analysis_id}")
    
    try:
        data = analysis_queue.get(analysis_id)
        if not data:
            print(f"❌ No data for {analysis_id}")
            return
            
        data["progress"] = 0.3
        data["message"] = "Fetching API documentation..."
        await asyncio.sleep(1)
        
        data["progress"] = 0.6
        data["message"] = "Analyzing endpoints..."
        await asyncio.sleep(1)
        
        # Mock result
        result = f"""# API Documentation Analysis

**URL:** {data['api_url']}
**Type:** {data['api_type']}
**Level:** {data['level']}

## Overview
This API provides endpoints for data access.

## Key Endpoints
- GET / - Returns documentation
- POST /data - Submits data

## Authentication
API key required in headers.
"""
        
        data["result"] = result
        data["status"] = "complete"
        data["progress"] = 1.0
        
    except Exception as e:
        print(f"❌ API background error: {e}")
        if analysis_id in analysis_queue:
            analysis_queue[analysis_id]["status"] = "error"
            analysis_queue[analysis_id]["error"] = str(e)


async def process_snippet_background(analysis_id: str):
    print(f"🚀 STARTING snippet background task for {analysis_id}")
    try:
        data = analysis_queue.get(analysis_id)
        if not data:
            print(f"❌ No data found for {analysis_id}")
            return
            
        print(f"📊 Initial data: {data}")
        
        # Update progress
        data["progress"] = 0.3
        data["message"] = "Processing..."
        
        # Simulate work
        await asyncio.sleep(2)
        
        data["progress"] = 0.8
        data["message"] = "Almost done..."
        
        await asyncio.sleep(1)
        
        # Set result
        data["result"] = "Analysis complete"
        data["status"] = "complete"
        data["progress"] = 1.0
        
        print(f"✅ Complete for {analysis_id}")
        
    except Exception as e:
        print(f"❌ ERROR in background task: {e}")
        import traceback
        traceback.print_exc()
        if analysis_id in analysis_queue:
            analysis_queue[analysis_id]["status"] = "error"
            analysis_queue[analysis_id]["error"] = str(e)

@router.post("/process-snippet")
async def process_snippet(
    request: Request,
    code: str = Form(...),
    language: str = Form("auto"),
    level: str = Form("professional"),
    specific_questions: str = Form(""),
    doc_type: str = Form("functions")
):
    """Analyze code snippet"""
    analysis_id = str(uuid.uuid4())
    
    # Store in queue
    from shared.queue import analysis_queue
    analysis_queue[analysis_id] = {
        "code": code[:10000],
        "language": language,
        "level": level,
        "specific_questions": specific_questions,
        "doc_type": doc_type,
        "status": "processing",
        "progress": 0.1,
        "message": "Starting code analysis...",
        "created_at": time.time()
    }
    
    # Start background task
    asyncio.create_task(run_analysis(analysis_id, data, prompt))
    
    # Redirect to loading page
    return RedirectResponse(url=f"/snippet-loading/{analysis_id}", status_code=303)

@router.get("/snippet-loading/{analysis_id}")
async def snippet_loading(analysis_id: str, request: Request):
    """Show loading page for snippet analysis"""
    from shared.queue import analysis_queue
    
    if analysis_id not in analysis_queue:
        return RedirectResponse(url="/snippet-analyzer", status_code=303)
    
    # Return loading page
    return await loading_response(analysis_id)

@router.post("/process-snippet")
async def process_snippet(
    request: Request,
    code: str = Form(...),
    language: str = Form("auto"),
    level: str = Form("professional"),
    specific_questions: str = Form(""),
    doc_type: str = Form("functions")
):
    print(f"🔥🔥🔥 HIT process-snippet with METHOD: {request.method}")
    if request.method == "GET":
        print(f"⚠️⚠️⚠️ GET request to process-snippet! Headers: {dict(request.headers)}")
        print(f"⚠️⚠️⚠️ Referrer: {request.headers.get('referer')}")
        # For now, redirect to the form
        return RedirectResponse(url="/snippet-analyzer", status_code=303)
    
    """Analyze code snippet and show results"""
    analysis_id = str(uuid.uuid4())
    
    from shared.queue import analysis_queue
    analysis_queue[analysis_id] = {
        "code": code[:10000],
        "language": language,
        "level": level,
        "specific_questions": specific_questions,
        "doc_type": doc_type,
        "status": "processing",
        "progress": 0.1,
        "message": "Starting code analysis...",
        "created_at": time.time()
    }
    
    # Start background task
    asyncio.create_task(analyze_snippet_background(analysis_id))
    
    # Go to loading page, NOT back to form
    return await loading_response(analysis_id)  # This should show loading, not form

def run_snippet_background(analysis_id: str):
    """Run in a separate thread (not async)"""
    print(f"🔥 THREAD started for {analysis_id}")
    
    try:
        import asyncio
        
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async function
        loop.run_until_complete(process_snippet_background(analysis_id))
        loop.close()
        
    except Exception as e:
        print(f"❌ Thread error: {e}")
        import traceback
        traceback.print_exc()

async def process_snippet_background(analysis_id: str):
    """Background task for snippet analysis"""
    print(f"🚀 Background task started for {analysis_id}")
    print(f"🔥🔥🔥 BACKGROUND TASK FIRED for {analysis_id} 🔥🔥🔥")
    print(f"Stack trace:", __import__('traceback').format_stack())
    
    try:
        # Get data from queue
        data = analysis_queue.get(analysis_id)
        if not data:
            print(f"❌ No data found for {analysis_id}")
            return
            
        # Update progress
        data["progress"] = 0.3
        data["message"] = "Parsing code structure..."
        await asyncio.sleep(1)
        
        data["progress"] = 0.6
        data["message"] = "Analyzing logic..."
        await asyncio.sleep(1)
        
        # Generate result
        lines = len(data['code'].split('\n'))
        result = f"""# Code Analysis Complete

**Language:** {data['language']}
**Lines:** {lines}
**Level:** {data['level']}

## Overview
Your code has been analyzed successfully.

## Key Findings
- The code appears to be well-structured
- Main logic handles core functionality
- Consider adding error handling

## Suggestions
1. Add input validation
2. Include comments for complex sections
3. Write tests for edge cases
"""
        
        # Store result
        data["result"] = result
        data["status"] = "complete"
        data["progress"] = 1.0
        data["message"] = "Complete!"
        
        print(f"✅ Snippet analysis complete for {analysis_id}")
        
    except Exception as e:
        print(f"❌ Error in snippet background task: {e}")
        import traceback
        traceback.print_exc()
        
        if analysis_id in analysis_queue:
            analysis_queue[analysis_id]["status"] = "error"
            analysis_queue[analysis_id]["error"] = str(e)

@router.get("/api/analysis-status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    print(f"🔍 STATUS CHECK for {analysis_id}")
    print(f"🔍 QUEUE HAS: {list(analysis_queue.keys())}")

    if analysis_id in analysis_queue:
        data = analysis_queue[analysis_id]
        return {
            "status": data.get("status", "processing"),
            "progress": data.get("progress", 0.1),
            "message": data.get("message", "Processing..."),
            "error": data.get("error")
        }
    return {"status": "not_found", "error": "Analysis not found"}

@router.get("/debug/check/{analysis_id}")
async def debug_check(analysis_id: str):
    if analysis_id in analysis_queue:
        return analysis_queue[analysis_id]
    return {"error": "not found", "queue": list(analysis_queue.keys())}

@router.get("/github-loading/{analysis_id}")
async def github_loading(analysis_id: str, request: Request):
    """Dedicated loading page for GitHub"""
    return await loading_response(analysis_id)

@router.post("/process-snippet")
async def process_snippet(
    request: Request,
    code: str = Form(...),
    language: str = Form("auto"),
    level: str = Form("professional"),
    specific_questions: str = Form(""),
    doc_type: str = Form("functions")
):
    """Process code snippet analysis"""
    
    analysis_id = str(uuid.uuid4())
    print(f"🔍 Processing snippet: {analysis_id}")
    
    # Build the prompt
    prompt = f"""Analyze this code for a {level} audience:

{code}

Focus on:
1. PURPOSE: What does this code do?
2. LOGIC: Key operations and flow
3. COMPLEXITY: Areas that need attention
4. EDGE CASES: Missing error handling
5. IMPROVEMENTS: How to make it better"""

    if specific_questions:
        prompt += f"\n\nSpecific questions: {specific_questions}"
    
    # CREATE data dictionary (NOT analysis_queue)
data = {
    "code": code[:10000],
    "language": language,
    "level": level,
    "specific_questions": specific_questions,
    "doc_type": doc_type,
    "status": "processing",
    "progress": 0.1,
    "message": "Starting code analysis...",
    "created_at": time.time()
}

print(f"📦 Data being saved: {list(data.keys())}")

# Save to file queue
from shared.file_queue import save_analysis
save_analysis(analysis_id, data)

# Start background task
from routes.analyzers.base import run_analysis
asyncio.create_task(run_analysis(analysis_id, data, prompt))

# Redirect to loading page
return RedirectResponse(url=f"/snippet-loading/{analysis_id}", status_code=303)