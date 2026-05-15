from datetime import date, datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Stramos Wisdom Charity API"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"


settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Humanitarian OS API for Stramos Wisdom Charity.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProgramCategory(str, Enum):
    orphan_support = "orphan_support"
    widow_support = "widow_support"
    youth_empowerment = "youth_empowerment"
    health_awareness = "health_awareness"
    blood_donation = "blood_donation"
    mental_health = "mental_health"
    refugee_outreach = "refugee_outreach"
    orphanage_partnerships = "orphanage_partnerships"
    women_in_tech = "women_in_tech"
    environmental_awareness = "environmental_awareness"
    partnerships = "partnerships"


class VolunteerCreate(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str = Field(min_length=7)
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    interests: list[ProgramCategory] = []
    message: Optional[str] = None


class PartnerCreate(BaseModel):
    organization_name: str = Field(min_length=2)
    contact_person: str = Field(min_length=2)
    phone: str = Field(min_length=7)
    email: Optional[EmailStr] = None
    partnership_area: ProgramCategory
    message: Optional[str] = None


class DonationIntent(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str = Field(min_length=7)
    amount_ugx: int = Field(gt=0)
    campaign: Optional[str] = None
    message: Optional[str] = None


class Event(BaseModel):
    slug: str
    title: str
    category: ProgramCategory
    summary: str
    target_month: Optional[str] = None


EVENTS = [
    Event(slug="run-for-hope", title="Stramos Run For Hope", category=ProgramCategory.youth_empowerment, summary="Community charity marathon/walk for awareness, mobilization, and support.", target_month="October"),
    Event(slug="lifeshare-blood-drive", title="Stramos LifeShare Blood Drive", category=ProgramCategory.blood_donation, summary="Blood donation and emergency health awareness drive."),
    Event(slug="mind-and-hope", title="Stramos Mind & Hope Conference", category=ProgramCategory.mental_health, summary="Mental health awareness, trauma healing, addiction awareness, and youth wellness."),
    Event(slug="future-builders", title="Stramos Future Builders Summit", category=ProgramCategory.youth_empowerment, summary="Youth mentorship, leadership, entrepreneurship, and practical skills."),
    Event(slug="refugee-hope", title="Stramos Refugee Hope Outreach", category=ProgramCategory.refugee_outreach, summary="Humanitarian support and dignity restoration for refugee communities."),
    Event(slug="women-in-tech", title="Stramos Women in Tech Summit", category=ProgramCategory.women_in_tech, summary="Girls and women digital inclusion, coding exposure, AI awareness, and cyber safety."),
    Event(slug="green-future", title="Stramos Green Future Initiative", category=ProgramCategory.environmental_awareness, summary="Environmental awareness, clean-up drives, tree planting, sanitation, and sustainability education."),
]

PROGRAMS = [
    {"title": "Orphan Support", "category": ProgramCategory.orphan_support, "summary": "Food, bedding, clothing, school support, emotional care, and orphanage visits."},
    {"title": "Widow & Vulnerable Family Support", "category": ProgramCategory.widow_support, "summary": "Welfare support, emergency aid, livelihood support, and empowerment."},
    {"title": "Youth Empowerment", "category": ProgramCategory.youth_empowerment, "summary": "Mentorship, discipline, entrepreneurship, leadership, digital literacy, and practical skills."},
    {"title": "Health & Awareness", "category": ProgramCategory.health_awareness, "summary": "Achieved and active health awareness programs including blood donation and mental health outreach."},
    {"title": "Refugee Outreach", "category": ProgramCategory.refugee_outreach, "summary": "Food, clothing, psychosocial support, children support, and dignity restoration."},
    {"title": "Orphanage Partnerships", "category": ProgramCategory.orphanage_partnerships, "summary": "Partnerships with children homes, shelters, and humanitarian centers."},
    {"title": "Women/Girls in Tech", "category": ProgramCategory.women_in_tech, "summary": "Digital inclusion, beginner coding, AI awareness, online work, and cyber safety."},
    {"title": "Environmental Awareness", "category": ProgramCategory.environmental_awareness, "summary": "Clean-up drives, tree planting, waste management, and school awareness."},
]

CONTACTS = {
    "email": "igahussein4@gmail.com",
    "phones": ["+256700709940", "+256783409327", "+256759902139"],
    "tiktok": "@stramoswisdomcharity",
    "slogan": "James 1:27 in Action",
    "public_message": "Love Wins",
}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "time": datetime.utcnow().isoformat()}


@app.get("/api/contact")
def get_contact() -> dict:
    return CONTACTS


@app.get("/api/programs")
def list_programs() -> list[dict]:
    return PROGRAMS


@app.get("/api/events", response_model=list[Event])
def list_events() -> list[Event]:
    return EVENTS


@app.get("/api/events/{slug}", response_model=Event)
def get_event(slug: str) -> Event:
    for event in EVENTS:
        if event.slug == slug:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/api/volunteers")
def create_volunteer(payload: VolunteerCreate) -> dict:
    return {"status": "received", "type": "volunteer", "data": payload.model_dump()}


@app.post("/api/partners")
def create_partner(payload: PartnerCreate) -> dict:
    return {"status": "received", "type": "partner", "data": payload.model_dump()}


@app.post("/api/donations/intent")
def create_donation_intent(payload: DonationIntent) -> dict:
    return {
        "status": "received",
        "type": "donation_intent",
        "payment_methods": ["MTN MoMo", "Airtel Money", "direct coordination"],
        "contacts": CONTACTS["phones"],
        "data": payload.model_dump(),
    }
