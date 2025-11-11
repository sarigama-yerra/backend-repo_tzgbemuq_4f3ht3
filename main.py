import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Application, BoardMember, Event, Announcement

app = FastAPI(title="School Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "School Club API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["collections"] = db.list_collection_names()
        else:
            response["database"] = "❌ Not Configured"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Helpers
class IdModel(BaseModel):
    id: str

def _id(obj):
    if isinstance(obj, dict) and obj.get("_id"):
        obj["id"] = str(obj.pop("_id"))
    return obj

# Applications
@app.post("/api/applications")
def create_application(apply: Application):
    try:
        inserted = create_document("application", apply)
        return {"id": inserted, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications")
def list_applications(status: Optional[str] = None, limit: int = 100):
    try:
        f = {"status": status} if status else {}
        docs = [_id(d) for d in get_documents("application", f, limit)]
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Board Members
@app.get("/api/board")
def get_board():
    try:
        docs = [_id(d) for d in get_documents("boardmember", {}, 50)]
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/board")
def add_board(member: BoardMember):
    try:
        inserted = create_document("boardmember", member)
        return {"id": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Events
@app.get("/api/events")
def list_events(limit: int = 50):
    try:
        docs = [_id(d) for d in get_documents("event", {"is_published": True}, limit)]
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/events")
def create_event(event: Event):
    try:
        inserted = create_document("event", event)
        return {"id": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Announcements
@app.get("/api/announcements")
def list_announcements(limit: int = 20):
    try:
        docs = [_id(d) for d in get_documents("announcement", {"is_published": True}, limit)]
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/announcements")
def create_announcement(ann: Announcement):
    try:
        inserted = create_document("announcement", ann)
        return {"id": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
