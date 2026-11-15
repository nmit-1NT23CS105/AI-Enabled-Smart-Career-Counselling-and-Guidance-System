# AI-Enabled Smart Career Counselling and Guidance System

Phase 1 implementation of a premium web-based career guidance system for students.

## Features

- Landing page with modern SaaS style
- User registration and login
- Local storage session handling
- Student dashboard
- Interactive career assessment form
- Dynamic academic-level based assessment wizard
- Fit-aware level-specific recommendation engine
- Top 5 career recommendations
- Match percentages, confidence labels, strengths, gaps, fit notes, and next steps
- Chart.js career match comparison chart
- JSON file storage

## Tech Stack

- Backend: FastAPI, Uvicorn, Pydantic
- Frontend: HTML5, CSS3, JavaScript
- Charts: Chart.js
- Storage: JSON files

## Project Structure

```text
career-guidance-system/
  frontend/
    index.html
    login.html
    register.html
    dashboard.html
    assessment.html
    results.html
    css/
      style.css
      dashboard.css
      assessment.css
    js/
      login.js
      register.js
      dashboard.js
      assessment.js
      results.js
    assets/
      images/
      icons/
        logo.svg
  backend/
    main.py
    routes/
      auth.py
      recommendation.py
    services/
      career_engine.py
      storage.py
    models/
      user.py
      assessment.py
    data/
      users.json
      careers.json
  requirements.txt
  README.md
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

4. Open the application:

```text
http://127.0.0.1:8000
```

## API Endpoints

- `POST /register`
- `POST /login`
- `POST /assessment`
- `GET /recommendations?user_id=<USER_ID>`
- `GET /health`

## Recommendation Logic

The engine selects a different dataset, assessment structure, and weighted scoring model for each academic level:

- High School: academic performance 30%, favorite subjects 25%, activities 20%, strength areas 25%
- Intermediate / PUC: subject marks 35%, interests 25%, skills 20%, career goal 20%
- Undergraduate: CGPA 20%, skills 30%, projects 15%, internships 15%, certifications 10%, interests 10%
- Job Seeker: experience 20%, skills 30%, projects 15%, certifications 15%, resume score 20%
- Higher Studies: CGPA 20%, subject marks 30%, research interests 20%, projects 15%, publications 15%

The recommendation engine is now `rule-v2-fit-aware`. It improves ranking quality with:

- Alias-aware matching for common variants such as AI / artificial intelligence, ML / machine learning, DSA / data structures and algorithms, and UI/UX / UI design.
- Core-skill weighting for undergraduate and job-seeker recommendations so critical skills count more than optional skills.
- Eligibility and fit caps so a high generic score does not over-rank paths with stream, degree, branch, goal, or core-skill gaps.
- Confidence labels such as Strong match, Good match, Exploratory match, Stretch path, and Low evidence.
- Fit notes that explain when a recommendation needs an eligibility transition or missing core preparation.
- Timeline guidance for undergraduate students based on current year.
- Preferred-country-aware higher-study guidance with country-specific exams and university ordering.

Each recommendation card includes match percentage, confidence label, fit status, why it was recommended, strengths detected, missing areas, fit notes, suggested next steps, dynamic score breakdown, and level-specific metrics.

## Assessment Payload

`POST /assessment` accepts a level-specific `data` object:

```json
{
  "user_id": "USER_ID",
  "academic_level": "Undergraduate Student",
  "data": {
    "degree": "B.Tech",
    "branch": "CSE",
    "cgpa": 8.4,
    "current_year": 3,
    "backlogs": 0,
    "technical_skills": ["Python", "SQL", "Machine Learning"],
    "certifications": ["AWS"],
    "projects": 3,
    "internships": 1,
    "career_interests": ["AI Engineer", "Data Scientist"]
  }
}
```

## Notes

- User credentials are stored in `backend/data/users.json` with salted PBKDF2 password hashes.
- Chart.js is loaded from a CDN on the results page.
- The JSON storage service is isolated in `backend/services/storage.py` so it can be replaced by MongoDB repositories later.
