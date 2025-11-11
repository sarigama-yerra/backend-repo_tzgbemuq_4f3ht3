"""
Database Schemas for School Club 3D Website

Each Pydantic model maps to a MongoDB collection using the lowercase class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Public applicant form (applications collection)
class Application(BaseModel):
    full_name: str = Field(..., description="Student's full name")
    email: EmailStr = Field(..., description="Student email")
    student_id: str = Field(..., description="Student number")
    department: str = Field(..., description="Department/Faculty")
    interests: List[str] = Field(default_factory=list, description="Interest tags")
    motivation: Optional[str] = Field(None, description="Motivation letter / notes")
    status: str = Field("pending", description="Application status: pending/approved/rejected")

# Management board (boardmember collection)
class BoardMember(BaseModel):
    name: str
    role: str = Field(..., description="e.g. Başkan, Başkan Yardımcısı, Sekreter")
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    socials: dict = Field(default_factory=dict, description="{instagram, linkedin, github, website}")

# Events (event collection)
class Event(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    banner_url: Optional[str] = None
    is_published: bool = True

# Announcements / News (announcement collection)
class Announcement(BaseModel):
    title: str
    content: str
    cover_url: Optional[str] = None
    is_published: bool = True
