from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


LEVEL_ALIASES = {
    "high school": "high_school",
    "high school (8th - 10th)": "high_school",
    "intermediate": "intermediate",
    "intermediate / puc": "intermediate",
    "intermediate / puc (11th - 12th)": "intermediate",
    "undergraduate": "undergraduate",
    "undergraduate student": "undergraduate",
    "job seeker": "job_seeker",
    "higher studies": "higher_studies",
    "higher studies aspirant": "higher_studies",
    "postgraduate": "higher_studies",
}

INTERMEDIATE_SUBJECTS = {
    "MPC": ["Mathematics", "Physics", "Chemistry"],
    "BiPC": ["Biology", "Physics", "Chemistry"],
    "MEC": ["Mathematics", "Economics", "Commerce"],
    "CEC": ["Civics", "Economics", "Commerce"],
    "HEC": ["History", "Economics", "Civics"],
}

HIGHER_STUDY_SUBJECTS = {
    "CSE": ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "AI", "Machine Learning", "Software Engineering"],
    "AIML": ["Data Structures", "AI", "Machine Learning", "Deep Learning", "Python", "Statistics"],
    "ECE": ["VLSI", "Signals", "Embedded Systems", "Digital Electronics"],
    "EEE": ["Power Systems", "Control Systems", "Electrical Machines", "Digital Electronics"],
    "Mechanical": ["Thermodynamics", "Manufacturing", "CAD", "Fluid Mechanics"],
    "Civil": ["Structures", "Surveying", "Geotechnical Engineering", "Construction Materials"],
    "IT": ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Software Engineering"],
}


def normalize_level(value: str) -> str | None:
    return LEVEL_ALIASES.get(value.strip().lower())


def _require_text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key.replace('_', ' ').title()} is required.")
    return value.strip()


def _require_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key.replace('_', ' ').title()} is required.")
    return value


def _require_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"Select at least one {key.replace('_', ' ')} option.")

    normalized = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if not normalized:
        raise ValueError(f"Select at least one {key.replace('_', ' ')} option.")
    return normalized


def _require_number(data: dict[str, Any], key: str, minimum: float | None = None, maximum: float | None = None) -> float:
    value = data.get(key)
    if value in ("", None):
        raise ValueError(f"{key.replace('_', ' ').title()} is required.")

    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{key.replace('_', ' ').title()} must be a number.") from error

    if minimum is not None and number < minimum:
        raise ValueError(f"{key.replace('_', ' ').title()} must be at least {minimum}.")
    if maximum is not None and number > maximum:
        raise ValueError(f"{key.replace('_', ' ').title()} must be at most {maximum}.")
    return number


def _validate_marks(marks: dict[str, Any], subjects: list[str]) -> None:
    for subject in subjects:
        _require_number(marks, subject, 0, 100)


def _validate_ratings(ratings: dict[str, Any], names: list[str]) -> None:
    for name in names:
        _require_number(ratings, name, 1, 5)


class AssessmentRequest(BaseModel):
    user_id: str = Field(..., min_length=8)
    academic_level: str = Field(..., min_length=2, max_length=80)
    data: dict[str, Any] = Field(default_factory=dict)

    @field_validator("user_id", "academic_level", mode="before")
    @classmethod
    def normalize_text(cls, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("This field is required.")
        return value.strip()

    @field_validator("data")
    @classmethod
    def data_must_be_object(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("Assessment data must be an object.")
        return value

    @model_validator(mode="after")
    def validate_level_specific_data(self) -> "AssessmentRequest":
        level_key = normalize_level(self.academic_level)
        if not level_key:
            raise ValueError("Select a supported academic level.")

        if level_key == "high_school":
            self._validate_high_school()
        elif level_key == "intermediate":
            self._validate_intermediate()
        elif level_key == "undergraduate":
            self._validate_undergraduate()
        elif level_key == "job_seeker":
            self._validate_job_seeker()
        elif level_key == "higher_studies":
            self._validate_higher_studies()

        return self

    def _validate_high_school(self) -> None:
        basic = _require_mapping(self.data, "basic_info")
        _require_text(basic, "name")
        _require_text(basic, "class_level")
        _require_text(basic, "school")

        marks = _require_mapping(self.data, "marks")
        _validate_marks(marks, ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Biology"])

        _require_list(self.data, "favorite_subjects")
        _require_list(self.data, "activities")

        strengths = _require_mapping(self.data, "strengths")
        _validate_ratings(strengths, ["Problem Solving", "Creativity", "Communication", "Leadership", "Teamwork", "Critical Thinking"])

    def _validate_intermediate(self) -> None:
        stream = _require_text(self.data, "stream")
        if stream not in INTERMEDIATE_SUBJECTS:
            raise ValueError("Select a supported Intermediate / PUC stream.")

        subject_marks = _require_mapping(self.data, "subject_marks")
        _validate_marks(subject_marks, INTERMEDIATE_SUBJECTS[stream])

        _require_list(self.data, "interest_areas")
        _require_list(self.data, "skills")

    def _validate_undergraduate(self) -> None:
        _require_text(self.data, "degree")
        _require_text(self.data, "branch")
        _require_number(self.data, "cgpa", 0, 10)
        _require_number(self.data, "current_year", 1, 6)
        _require_number(self.data, "backlogs", 0, 30)
        _require_list(self.data, "technical_skills")
        _require_list(self.data, "career_interests")
        _require_number(self.data, "projects", 0, 100)
        _require_number(self.data, "internships", 0, 50)
        if not isinstance(self.data.get("certifications", []), list):
            raise ValueError("Certifications must be a list.")

    def _validate_job_seeker(self) -> None:
        education = _require_mapping(self.data, "education")
        _require_text(education, "degree")
        _require_text(education, "branch")
        _require_number(education, "cgpa", 0, 10)

        _require_number(self.data, "experience_years", 0, 50)
        _require_list(self.data, "current_skills")
        _require_number(self.data, "projects", 0, 100)
        if not isinstance(self.data.get("certifications", []), list):
            raise ValueError("Certifications must be a list.")

        resume = _require_mapping(self.data, "resume")
        _require_text(resume, "file_name")
        _require_text(self.data, "preferred_industry")
        _require_text(self.data, "preferred_location")
        _require_number(self.data, "expected_salary", 0, None)

    def _validate_higher_studies(self) -> None:
        _require_text(self.data, "degree")
        branch = _require_text(self.data, "branch")
        _require_number(self.data, "cgpa", 0, 10)

        subject_marks = _require_mapping(self.data, "subject_marks")
        _validate_marks(subject_marks, HIGHER_STUDY_SUBJECTS.get(branch, ["Core Subject 1", "Core Subject 2", "Core Subject 3"]))

        _require_list(self.data, "research_interests")
        _require_number(self.data, "research_publications", 0, 100)
        _require_number(self.data, "projects", 0, 100)
        _require_text(self.data, "higher_study_goal")
        _require_text(self.data, "preferred_country")
