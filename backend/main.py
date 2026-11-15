from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routes import auth, recommendation


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="AI-Enabled Smart Career Counselling and Guidance System",
    description="Phase 1 FastAPI backend for student career recommendations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recommendation.router)

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")


def _serve_page(filename: str) -> FileResponse:
    return FileResponse(FRONTEND_DIR / filename)


@app.get("/")
def landing_page() -> FileResponse:
    return _serve_page("index.html")


@app.get("/login")
@app.get("/login.html")
def login_page() -> FileResponse:
    return _serve_page("login.html")


@app.get("/register")
@app.get("/register.html")
def register_page() -> FileResponse:
    return _serve_page("register.html")


@app.get("/dashboard")
@app.get("/dashboard.html")
def dashboard_page() -> FileResponse:
    return _serve_page("dashboard.html")


@app.get("/assessment")
@app.get("/assessment.html")
def assessment_page() -> FileResponse:
    return _serve_page("assessment.html")


@app.get("/results")
@app.get("/results.html")
def results_page() -> FileResponse:
    return _serve_page("results.html")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
