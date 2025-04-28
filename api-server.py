"""
LinkedIn Profile Query Bot API

This module provides a FastAPI server that serves as an API for the LinkedIn Profile Query Bot.
"""

import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
import json
from query_processor import ProfileQueryProcessor

app = FastAPI(
    title="LinkedIn Profile Query Bot API",
    description="API for processing natural language queries about LinkedIn profiles",
    version="1.0.0"
)

# Initialize the query processor
processor = ProfileQueryProcessor(profiles_dir="profiles")

class QueryRequest(BaseModel):
    """Request model for profile queries."""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class WatiRequest(BaseModel):
    """Request model for Wati webhook integration."""
    event: str
    userData: Dict[str, Any]
    payload: Dict[str, Any]

class ProfileSummary(BaseModel):
    """Model for profile summary response."""
    profile_id: str
    name: str
    headline: Optional[str] = None

@app.get("/")
async def root():
    """API root endpoint."""
    return {"message": "LinkedIn Profile Query Bot API"}

@app.get("/profiles", response_model=List[ProfileSummary])
async def list_profiles():
    """List all available profiles."""
    profiles = []
    
    # Get profiles from processor's loaded profiles
    for profile_id, profile_data in processor.loaded_profiles.items():
        profiles.append({
            "profile_id": profile_id,
            "name": profile_data["basics"]["name"],
            "headline": profile_data["basics"].get("headline")
        })
    
    return profiles

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process a query about a LinkedIn profile."""
    try:
        result = processor.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wati-webhook")
async def wati_webhook(request: WatiRequest = Body(...)):
    """
    Webhook endpoint for Wati integration.
    
    This endpoint receives messages from Wati and processes LinkedIn profile queries.
    """
    try:
        # Check if this is a message event
        if request.event != "message":
            return {"status": "ignored", "reason": "Not a message event"}
        
        # Extract message text
        message_text = request.payload.get("text", "")
        if not message_text:
            return {"status": "ignored", "reason": "No message text"}
        
        # Process the query
        result = processor.process_query(message_text)
        
        # Prepare response for Wati
        if result["success"]:
            response_text = result["response"]
        else:
            available_profiles = ", ".join(result.get("available_profiles", []))
            response_text = f"{result['error']}. Available profiles: {available_profiles}"
        
        # In a real implementation, this would send a response back to Wati API
        # Here we just return what would be sent
        return {
            "status": "success",
            "response": response_text,
            "whatsapp_number": request.userData.get("waId"),
            "query_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-profile")
async def add_profile(profile_data: Dict[str, Any] = Body(...)):
    """
    Add a new LinkedIn profile to the system.
    
    In a real implementation, this would validate and process the profile data.
    """
    try:
        # Validate required fields
        if not profile_data.get("profile_id"):
            raise HTTPException(status_code=400, detail="profile_id is required")
        
        if not profile_data.get("basics") or not profile_data["basics"].get("name"):
            raise HTTPException(status_code=400, detail="basics.name is required")
        
        # Save profile to file
        profile_id = profile_data["profile_id"]
        profile_file = os.path.join(processor.profiles_dir, f"{profile_id}.json")
        
        # Create directory if it doesn't exist
        os.makedirs(processor.profiles_dir, exist_ok=True)
        
        # Write profile data to file
        with open(profile_file, "w") as f:
            json.dump(profile_data, f, indent=2)
        
        # Reload profile in processor
        processor._load_profile(profile_id)
        
        return {"status": "success", "profile_id": profile_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create profiles directory if it doesn't exist
    os.makedirs("profiles", exist_ok=True)
    
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
