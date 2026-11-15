import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, status

from backend.models.assessment import AssessmentRequest, normalize_level
from backend.services.career_engine import recommend_careers
from backend.services.storage import store


router = APIRouter(tags=["Recommendations"])


@router.post("/assessment", status_code=status.HTTP_201_CREATED)
def submit_assessment(payload: AssessmentRequest) -> dict:
    user = store.find_user_by_id(payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account was not found. Please log in again.",
        )

    dataset = store.read_careers()
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Career dataset is unavailable.",
        )

    assessment_data = payload.model_dump()
    assessment_data["level_key"] = normalize_level(payload.academic_level)

    try:
        engine_result = recommend_careers(assessment_data, dataset, limit=5)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    recommendations = engine_result["recommendations"]
    created_at = datetime.now(timezone.utc).isoformat()

    record = {
        "assessment_id": str(uuid.uuid4()),
        "created_at": created_at,
        "academic_level": payload.academic_level,
        "level_key": assessment_data["level_key"],
        "method_version": engine_result.get("method_version"),
        "data": payload.data,
        "weights": engine_result["weights"],
        "profile_summary": engine_result["profile_summary"],
        "recommendations": recommendations,
    }

    user.setdefault("assessments", []).insert(0, record)
    user["latest_recommendations"] = recommendations
    user["latest_assessment_level"] = payload.academic_level
    user["latest_profile_summary"] = engine_result["profile_summary"]
    user["latest_method_version"] = engine_result.get("method_version")
    user["last_assessment_at"] = created_at
    store.save_user(user)

    return {
        "message": "Assessment processed successfully.",
        "assessment_id": record["assessment_id"],
        "created_at": created_at,
        "academic_level": engine_result["academic_level"],
        "method_version": engine_result.get("method_version"),
        "weights": engine_result["weights"],
        "profile_summary": engine_result["profile_summary"],
        "recommendations": recommendations,
    }


@router.get("/recommendations")
def get_recommendations(user_id: str = Query(..., min_length=8)) -> dict:
    user = store.find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account was not found. Please log in again.",
        )

    return {
        "user_id": user_id,
        "last_assessment_at": user.get("last_assessment_at"),
        "academic_level": user.get("latest_assessment_level"),
        "method_version": user.get("latest_method_version"),
        "profile_summary": user.get("latest_profile_summary"),
        "recommendations": user.get("latest_recommendations", []),
    }
