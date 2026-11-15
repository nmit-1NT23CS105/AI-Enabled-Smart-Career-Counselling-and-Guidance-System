from typing import Any

from backend.models.assessment import normalize_level


TERM_ALIASES = {
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "dl": "deep learning",
    "deep learning": "deep learning",
    "data structures": "dsa",
    "data structures and algorithms": "dsa",
    "dsa": "dsa",
    "web dev": "web development",
    "frontend": "web development",
    "front end": "web development",
    "backend": "web development",
    "back end": "web development",
    "full stack": "web development",
    "fullstack": "web development",
    "cybersecurity": "cyber security",
    "cyber security": "cyber security",
    "cloud": "cloud computing",
    "cloud computing": "cloud computing",
    "amazon web services": "aws",
    "azure": "microsoft",
    "ms azure": "microsoft",
    "google cloud": "google",
    "gcp": "google",
    "powerbi": "power bi",
    "power bi": "power bi",
    "ui ux": "ui design",
    "ux": "ui design",
    "ui": "ui design",
}

BRANCH_ALIASES = {
    "computer science": "cse",
    "computer applications": "it",
    "information technology": "it",
    "data science": "aiml",
    "cloud computing": "it",
    "business analytics": "business analytics",
    "finance": "commerce",
}

UNIVERSITY_COUNTRIES = {
    "IISc Bengaluru": "India",
    "IIT Hyderabad": "India",
    "IIIT Hyderabad": "India",
    "IIT Madras": "India",
    "IIIT Bangalore": "India",
    "IIT Kanpur": "India",
    "NIT Trichy": "India",
    "IIT Bombay": "India",
    "IIM Ahmedabad": "India",
    "IIM Bangalore": "India",
    "ISB": "India",
    "Carnegie Mellon University": "USA",
    "University of Washington": "USA",
    "University of Maryland": "USA",
    "Arizona State University": "USA",
    "MIT": "USA",
    "Stanford University": "USA",
    "University of Toronto": "Canada",
    "University of Waterloo": "Canada",
    "Rotman School of Management": "Canada",
    "TU Munich": "Germany",
    "TU Dresden": "Germany",
    "London Business School": "UK",
    "University of Cambridge": "UK",
}

COUNTRY_GUIDANCE = {
    "India": {
        "exams": ["GATE", "CAT", "CUET PG", "Institute entrance tests"],
        "next_step": "Shortlist Indian programs by entrance exam, cutoff, fees, and placement outcomes.",
    },
    "USA": {
        "exams": ["GRE", "TOEFL", "IELTS"],
        "next_step": "Prepare SOP, recommendation letters, test scores, and assistantship-ready project evidence.",
    },
    "UK": {
        "exams": ["IELTS", "TOEFL", "GMAT for MBA"],
        "next_step": "Compare one-year program fit, scholarship deadlines, and portfolio or SOP requirements.",
    },
    "Germany": {
        "exams": ["IELTS", "TOEFL", "GRE if required"],
        "next_step": "Check German program prerequisites, APS requirements, language rules, and blocked-account planning.",
    },
    "Canada": {
        "exams": ["IELTS", "TOEFL", "GRE if required"],
        "next_step": "Shortlist programs by research fit, co-op availability, funding, and application deadlines.",
    },
    "Australia": {
        "exams": ["IELTS", "TOEFL", "PTE"],
        "next_step": "Compare programs by accreditation, scholarship windows, employability, and visa requirements.",
    },
}


def _normalize(value: str) -> str:
    cleaned = str(value).replace("/", " ").replace("-", " ").replace("_", " ")
    return " ".join(cleaned.strip().lower().split())


def _canonical(value: str) -> str:
    normalized = _normalize(value)
    return TERM_ALIASES.get(normalized, normalized)


def _canonical_with_alias(value: str, aliases: dict[str, str]) -> str:
    normalized = _normalize(value)
    return aliases.get(normalized, _canonical(value))


def _matches_any(value: str, options: list[str], aliases: dict[str, str] | None = None) -> bool:
    if aliases is None:
        return _canonical(value) in {_canonical(option) for option in options}
    return _canonical_with_alias(value, aliases) in {_canonical_with_alias(option, aliases) for option in options}


def _unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        normalized = _canonical(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(value)
    return result


def _as_number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _overlap_score(selected: list[str], required: list[str], weight: float) -> tuple[float, list[str], list[str]]:
    if not required:
        return weight, [], []

    selected_lookup = {_canonical(item) for item in selected}
    matched = [item for item in required if _canonical(item) in selected_lookup]
    missing = [item for item in required if _canonical(item) not in selected_lookup]
    return (len(matched) / len(required)) * weight, matched, missing


def _weighted_overlap_score(
    selected: list[str],
    required: list[str],
    weight: float,
    core_items: list[str] | None = None,
) -> tuple[float, list[str], list[str]]:
    if not required:
        return weight, [], []

    selected_lookup = {_canonical(item) for item in selected}
    core_lookup = {_canonical(item) for item in core_items or []}
    total = 0.0
    matched_total = 0.0
    matched = []
    missing = []

    for item in required:
        item_weight = 2.0 if _canonical(item) in core_lookup else 1.0
        total += item_weight
        if _canonical(item) in selected_lookup:
            matched_total += item_weight
            matched.append(item)
        else:
            missing.append(item)

    return (matched_total / total) * weight, matched, missing


def _mark_score(marks: dict[str, Any], subjects: list[str], weight: float) -> tuple[float, list[str], list[str]]:
    if not subjects:
        values = [_as_number(value) for value in marks.values()]
    else:
        values = [_as_number(marks.get(subject)) for subject in subjects if subject in marks]

    if not values:
        return 0.0, [], subjects

    average = sum(values) / len(values)
    coverage = len(values) / len(subjects) if subjects else 1
    coverage_factor = 0.7 + (0.3 * coverage)
    strong = [subject for subject in subjects if subject in marks and _as_number(marks.get(subject)) >= 75]
    weak = [subject for subject in subjects if subject not in marks or _as_number(marks.get(subject)) < 65]
    return _clamp(average) / 100 * weight * coverage_factor, strong, weak


def _rating_score(ratings: dict[str, Any], strengths: list[str], weight: float) -> tuple[float, list[str], list[str]]:
    if not strengths:
        return weight, [], []

    values = [_as_number(ratings.get(item), 0) for item in strengths]
    average = sum(values) / len(values)
    strong = [item for item in strengths if _as_number(ratings.get(item)) >= 4]
    weak = [item for item in strengths if _as_number(ratings.get(item)) <= 2]
    return _clamp(average, 0, 5) / 5 * weight, strong, weak


def _cgpa_score(cgpa: Any, weight: float) -> float:
    return _clamp(_as_number(cgpa), 0, 10) / 10 * weight


def _count_score(count: Any, target: int, weight: float) -> float:
    if target <= 0:
        return weight
    return min(_as_number(count) / target, 1.0) * weight


def _text_score(text: str, keywords: list[str], weight: float, neutral_ratio: float = 0.4) -> tuple[float, list[str], list[str]]:
    if not text or not text.strip():
        return weight * neutral_ratio, [], keywords[:3]

    normalized = _expanded_text(text)
    matched = [keyword for keyword in keywords if _normalize(keyword) in normalized or _canonical(keyword) in normalized]
    if not keywords:
        return weight, matched, []
    return max(len(matched) / len(keywords), neutral_ratio) * weight, matched, [item for item in keywords if item not in matched]


def _expanded_text(text: str) -> str:
    normalized = _normalize(text)
    expanded_terms = [normalized]
    for alias, canonical in TERM_ALIASES.items():
        if alias in normalized:
            expanded_terms.append(canonical)
    return " ".join(expanded_terms)


def _listify(value: Any) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item.strip()]
    return []


def _build_reason(name: str, strengths: list[str], missing: list[str], fit_notes: list[str]) -> str:
    if strengths:
        reason = f"{name} is recommended because the assessment shows strength in {', '.join(strengths[:4])}."
    else:
        reason = f"{name} is the closest fit based on the available assessment signals."

    if missing:
        reason += f" Improving {', '.join(missing[:3])} can raise the match score."
    if fit_notes:
        reason += f" Fit note: {fit_notes[0]}"
    return reason


def _confidence_label(score: float, fit_blockers: list[str]) -> str:
    if fit_blockers:
        return "Stretch path"
    if score >= 82:
        return "Strong match"
    if score >= 68:
        return "Good match"
    if score >= 52:
        return "Exploratory match"
    return "Low evidence"


def _fit_status(fit_notes: list[str], fit_blockers: list[str]) -> str:
    if fit_blockers:
        return "Needs eligibility work"
    if fit_notes:
        return "Partially aligned"
    return "Aligned"


def _cap_score(
    score: float,
    cap: float,
    note: str,
    fit_notes: list[str],
    fit_blockers: list[str] | None = None,
) -> float:
    fit_notes.append(note)
    if fit_blockers is not None:
        fit_blockers.append(note)
    return min(score, cap)


def _core_items(criteria: dict[str, Any], key: str = "skills", count: int = 2) -> list[str]:
    configured = criteria.get("core_skills") or criteria.get("critical_skills")
    if configured:
        return configured[:count]
    return criteria.get(key, [])[:count]


def _missing_core_items(core_items: list[str], matched_items: list[str]) -> list[str]:
    matched_lookup = {_canonical(item) for item in matched_items}
    return [item for item in core_items if _canonical(item) not in matched_lookup]


def _undergrad_timeline(current_year: Any) -> str:
    year = _as_number(current_year)
    if year <= 2:
        return "Build fundamentals now: finish two portfolio projects before applying for internships."
    if year <= 4:
        return "Prioritize internships, interview practice, and deployable projects this academic year."
    return "Convert existing work into resume-ready case studies and start role-specific applications."


def _country_guidance(country: str) -> dict[str, Any]:
    return COUNTRY_GUIDANCE.get(country, {
        "exams": ["Program-specific entrance tests"],
        "next_step": "Check program prerequisites, deadlines, tests, funding, and visa requirements for the target country.",
    })


def _rank_universities(universities: list[str], preferred_country: str) -> list[str]:
    if not preferred_country:
        return universities
    preferred = [name for name in universities if UNIVERSITY_COUNTRIES.get(name) == preferred_country]
    others = [name for name in universities if UNIVERSITY_COUNTRIES.get(name) != preferred_country]
    return preferred + others


def _result(
    recommendation: dict[str, Any],
    score: float,
    breakdown: dict[str, float],
    strengths: list[str],
    missing: list[str],
    next_steps: list[str],
    metrics: dict[str, Any] | None = None,
    fit_notes: list[str] | None = None,
    fit_blockers: list[str] | None = None,
    raw_score: float | None = None,
) -> dict[str, Any]:
    name = recommendation["name"]
    fit_notes = _unique(fit_notes or [])
    fit_blockers = _unique(fit_blockers or [])
    cleaned_strengths = _unique(strengths) or ["Consistent overall profile"]
    cleaned_missing = _unique(missing) or ["No major gaps detected"]
    final_score = round(_clamp(score), 2)

    return {
        "career_name": name,
        "recommendation_name": name,
        "match_score": final_score,
        "confidence_label": _confidence_label(final_score, fit_blockers),
        "fit_status": _fit_status(fit_notes, fit_blockers),
        "fit_notes": fit_notes[:5],
        "description": recommendation["description"],
        "why_recommended": _build_reason(name, cleaned_strengths, missing, fit_notes),
        "strengths_detected": cleaned_strengths[:7],
        "missing_areas": cleaned_missing[:7],
        "suggested_next_steps": next_steps[:6],
        "breakdown": {key: round(value, 2) for key, value in breakdown.items()},
        "score_details": {
            "raw_score": round(_clamp(raw_score if raw_score is not None else score), 2),
            "final_score": final_score,
            "capped_by_fit": raw_score is not None and _clamp(raw_score) > final_score,
        },
        "metrics": metrics or {},
    }


def _score_high_school(data: dict[str, Any], level: dict[str, Any], limit: int) -> dict[str, Any]:
    weights = level["weights"]
    marks = data["marks"]
    favorite_subjects = _listify(data.get("favorite_subjects"))
    activities = _listify(data.get("activities"))
    ratings = data["strengths"]
    results = []

    for recommendation in level["recommendations"]:
        criteria = recommendation["criteria"]
        academic_score, strong_subjects, weak_subjects = _mark_score(marks, criteria["subjects"], weights["academic_performance"])
        subject_score, matched_subjects, missing_subjects = _overlap_score(favorite_subjects, criteria["favorite_subjects"], weights["favorite_subjects"])
        activity_score, matched_activities, missing_activities = _overlap_score(activities, criteria["activities"], weights["activities"])
        strength_score, strong_traits, weak_traits = _rating_score(ratings, criteria["strengths"], weights["strength_areas"])

        strengths = strong_subjects + matched_subjects + matched_activities + strong_traits
        missing = weak_subjects + missing_subjects + missing_activities + weak_traits
        breakdown = {
            "Academic Performance": academic_score,
            "Favorite Subjects": subject_score,
            "Activities": activity_score,
            "Strength Areas": strength_score,
        }
        metrics = {
            "Strength Analysis": strengths[:5],
            "Areas for Improvement": missing[:5],
            "Suggested Activities": recommendation.get("suggested_activities", []),
        }

        results.append(_result(recommendation, sum(breakdown.values()), breakdown, strengths, missing, recommendation["next_steps"], metrics))

    return _package(level, results, limit)


def _score_intermediate(data: dict[str, Any], level: dict[str, Any], limit: int) -> dict[str, Any]:
    weights = level["weights"]
    stream = data["stream"]
    marks = data["subject_marks"]
    interests = _listify(data.get("interest_areas"))
    skills = _listify(data.get("skills"))
    career_goal = data.get("career_goal", "")
    results = []

    for recommendation in level["recommendations"]:
        criteria = recommendation["criteria"]
        stream_fit = stream in criteria["streams"]
        stream_bonus = weights["subject_marks"] if stream_fit else weights["subject_marks"] * 0.35
        marks_score, strong_subjects, weak_subjects = _mark_score(marks, criteria["subjects"], stream_bonus)
        interest_score, matched_interests, missing_interests = _overlap_score(interests, criteria["interests"], weights["interests"])
        skill_score, matched_skills, missing_skills = _overlap_score(skills, criteria["skills"], weights["skills"])
        goal_score, goal_matches, goal_gaps = _text_score(career_goal, criteria["keywords"], weights["career_goal"])

        strengths = strong_subjects + matched_interests + matched_skills + goal_matches
        missing = weak_subjects + missing_interests + missing_skills + goal_gaps
        fit_notes: list[str] = []
        fit_blockers: list[str] = []
        breakdown = {
            "Subject Marks": marks_score,
            "Interests": interest_score,
            "Skills": skill_score,
            "Career Goal": goal_score,
        }
        raw_score = sum(breakdown.values())
        final_score = raw_score
        if not stream_fit:
            note = f"Required stream alignment: {', '.join(criteria['streams'])}"
            final_score = _cap_score(final_score, 58, note, fit_notes, fit_blockers)
            missing.append(note)
        metrics = {
            "Recommended Degrees": [recommendation["name"]],
            "Recommended Entrance Exams": recommendation.get("exams", []),
            "Required Skills": recommendation.get("required_skills", []),
            "Eligibility Fit": "Stream aligned" if stream_fit else "Stream transition required",
        }

        results.append(_result(
            recommendation,
            final_score,
            breakdown,
            strengths,
            missing,
            recommendation["next_steps"],
            metrics,
            fit_notes,
            fit_blockers,
            raw_score,
        ))

    return _package(level, results, limit)


def _score_undergraduate(data: dict[str, Any], level: dict[str, Any], limit: int) -> dict[str, Any]:
    weights = level["weights"]
    degree = data["degree"]
    branch = data["branch"]
    skills = _listify(data.get("technical_skills"))
    certifications = _listify(data.get("certifications"))
    interests = _listify(data.get("career_interests"))
    results = []

    for recommendation in level["recommendations"]:
        criteria = recommendation["criteria"]
        core_skills = _core_items(criteria)
        cgpa_score = _cgpa_score(data["cgpa"], weights["cgpa"])
        skill_score, matched_skills, missing_skills = _weighted_overlap_score(skills, criteria["skills"], weights["skills"], core_skills)
        project_score = _count_score(data["projects"], criteria["projects_target"], weights["projects"])
        internship_score = _count_score(data["internships"], criteria["internships_target"], weights["internships"])
        cert_score, matched_certs, missing_certs = _overlap_score(certifications, criteria["certifications"], weights["certifications"])
        interest_score, matched_interests, missing_interests = _overlap_score(interests, criteria["interests"], weights["interests"])

        degree_fit = _matches_any(degree, criteria["degrees"])
        branch_fit = _matches_any(branch, criteria["branches"], BRANCH_ALIASES)
        fit_bonus = 4 if degree_fit and branch_fit else 0
        fit_notes: list[str] = []
        fit_blockers: list[str] = []
        missing_core_skills = _missing_core_items(core_skills, matched_skills)

        strengths = matched_skills + matched_certs + matched_interests
        if _as_number(data["cgpa"]) >= 7.5:
            strengths.append("CGPA")
        if _as_number(data["projects"]) >= criteria["projects_target"]:
            strengths.append("Project portfolio")
        if _as_number(data["internships"]) >= criteria["internships_target"]:
            strengths.append("Internship exposure")

        missing = missing_skills + missing_certs + missing_interests
        if missing_core_skills:
            fit_notes.append(f"Core skill focus: {', '.join(missing_core_skills)}")
        if not branch_fit:
            missing.append(f"Branch alignment for {recommendation['name']}")
        if _as_number(data["backlogs"]) > 0:
            missing.append("Backlog clearance")

        breakdown = {
            "CGPA": cgpa_score,
            "Skills": skill_score,
            "Projects": project_score,
            "Internships": internship_score,
            "Certifications": cert_score,
            "Interests": interest_score,
        }
        raw_score = sum(breakdown.values()) + fit_bonus
        final_score = raw_score
        if not degree_fit:
            final_score = _cap_score(
                final_score,
                68,
                f"Best degree fit: {', '.join(criteria['degrees'])}",
                fit_notes,
                fit_blockers,
            )
        if not branch_fit:
            final_score = _cap_score(
                final_score,
                82,
                f"Branch transition needed from {branch} into {recommendation['name']}",
                fit_notes,
            )
        if len(missing_core_skills) == len(core_skills) and core_skills:
            final_score = _cap_score(
                final_score,
                72,
                f"Build at least one core skill for {recommendation['name']} before treating it as a primary path.",
                fit_notes,
            )
        placement_readiness = _clamp(final_score)
        timeline_guidance = _undergrad_timeline(data.get("current_year"))
        metrics = {
            "Placement Readiness Score": round(placement_readiness, 2),
            "Core Skills Required": core_skills,
            "Skill Gap Analysis": missing_skills[:5],
            "Recommended Certifications": recommendation.get("recommended_certifications", []),
            "Recommended Projects": recommendation.get("recommended_projects", []),
            "Internship Suggestions": recommendation.get("internship_suggestions", []),
            "Timeline Guidance": timeline_guidance,
        }

        results.append(_result(
            recommendation,
            final_score,
            breakdown,
            strengths,
            missing,
            recommendation["next_steps"] + [timeline_guidance],
            metrics,
            fit_notes,
            fit_blockers,
            raw_score,
        ))

    return _package(level, results, limit)


def _resume_score(data: dict[str, Any], required_skills: list[str], projects_target: int) -> float:
    resume = data.get("resume", {})
    score = 0.0
    if resume.get("file_name"):
        score += 35
    skill_score, _, _ = _overlap_score(_listify(data.get("current_skills")), required_skills, 30)
    score += skill_score
    score += _count_score(data.get("projects"), projects_target, 20)
    if _listify(data.get("certifications")):
        score += 10
    if data.get("preferred_location") and data.get("expected_salary") is not None:
        score += 5
    return _clamp(score)


def _score_job_seeker(data: dict[str, Any], level: dict[str, Any], limit: int) -> dict[str, Any]:
    weights = level["weights"]
    skills = _listify(data.get("current_skills"))
    certifications = _listify(data.get("certifications"))
    preferred_industry = data["preferred_industry"]
    results = []

    for recommendation in level["recommendations"]:
        criteria = recommendation["criteria"]
        core_skills = _core_items(criteria)
        experience_score = _count_score(data["experience_years"], criteria["experience_target"], weights["experience"])
        skill_score, matched_skills, missing_skills = _weighted_overlap_score(skills, criteria["skills"], weights["skills"], core_skills)
        project_score = _count_score(data["projects"], criteria["projects_target"], weights["projects"])
        cert_score, matched_certs, missing_certs = _overlap_score(certifications, criteria["certifications"], weights["certifications"])
        resume_quality = _resume_score(data, criteria["skills"], criteria["projects_target"])
        resume_component = resume_quality / 100 * weights["resume_score"]
        industry_bonus = 4 if preferred_industry in criteria["industries"] else 0
        fit_notes: list[str] = []
        fit_blockers: list[str] = []
        missing_core_skills = _missing_core_items(core_skills, matched_skills)

        strengths = matched_skills + matched_certs
        if _as_number(data["experience_years"]) >= criteria["experience_target"]:
            strengths.append("Relevant experience")
        if preferred_industry in criteria["industries"]:
            strengths.append("Industry preference alignment")

        missing = missing_skills + missing_certs
        if missing_core_skills:
            fit_notes.append(f"Core skill focus: {', '.join(missing_core_skills)}")
        if resume_quality < 70:
            missing.append("ATS-focused resume structure")
        if preferred_industry not in criteria["industries"]:
            fit_notes.append(f"Industry transition from {preferred_industry} toward {', '.join(criteria['industries'][:3])}")

        breakdown = {
            "Experience": experience_score,
            "Skills": skill_score,
            "Projects": project_score,
            "Certifications": cert_score,
            "Resume Score": resume_component,
        }
        raw_score = sum(breakdown.values()) + industry_bonus
        final_score = raw_score
        if len(missing_core_skills) == len(core_skills) and core_skills:
            final_score = _cap_score(
                final_score,
                74,
                f"Build at least one core skill for {recommendation['name']} before prioritizing applications.",
                fit_notes,
            )
        metrics = {
            "Job Readiness Score": round(_clamp(final_score), 2),
            "ATS Readiness Score": round(resume_quality, 2),
            "Suitable Job Roles": [recommendation["name"]],
            "Core Skills Required": core_skills,
            "Missing Skills": missing_skills[:5],
            "Resume Improvement Suggestions": recommendation.get("resume_suggestions", []),
            "Preference Fit": "Industry aligned" if preferred_industry in criteria["industries"] else "Industry transition",
            "Location Preference": data.get("preferred_location", "Not specified"),
        }

        results.append(_result(
            recommendation,
            final_score,
            breakdown,
            strengths,
            missing,
            recommendation["next_steps"],
            metrics,
            fit_notes,
            fit_blockers,
            raw_score,
        ))

    return _package(level, results, limit)


def _score_higher_studies(data: dict[str, Any], level: dict[str, Any], limit: int) -> dict[str, Any]:
    weights = level["weights"]
    marks = data["subject_marks"]
    interests = _listify(data.get("research_interests"))
    goal = data["higher_study_goal"]
    preferred_country = data.get("preferred_country", "")
    results = []

    for recommendation in level["recommendations"]:
        criteria = recommendation["criteria"]
        cgpa_score = _cgpa_score(data["cgpa"], weights["cgpa"])
        subject_score, strong_subjects, weak_subjects = _mark_score(marks, criteria["subjects"], weights["subject_marks"])
        interest_score, matched_interests, missing_interests = _overlap_score(interests, criteria["research_interests"], weights["research_interests"])
        project_score = _count_score(data["projects"], criteria["projects_target"], weights["projects"])
        publication_score = _count_score(data["research_publications"], criteria["publications_target"], weights["publications"])
        goal_bonus = 4 if goal in criteria["goals"] else 0
        fit_notes: list[str] = []
        fit_blockers: list[str] = []

        strengths = strong_subjects + matched_interests
        if _as_number(data["projects"]) >= criteria["projects_target"]:
            strengths.append("Research projects")
        if _as_number(data["research_publications"]) >= criteria["publications_target"]:
            strengths.append("Publication record")

        missing = weak_subjects + missing_interests
        if goal not in criteria["goals"]:
            missing.append(f"Goal alignment for {recommendation['name']}")
            fit_notes.append(f"Best goal fit: {', '.join(criteria['goals'])}")

        breakdown = {
            "CGPA": cgpa_score,
            "Subject Marks": subject_score,
            "Research Interests": interest_score,
            "Projects": project_score,
            "Publications": publication_score,
        }
        raw_score = sum(breakdown.values()) + goal_bonus
        final_score = raw_score
        if goal not in criteria["goals"]:
            final_score = _cap_score(
                final_score,
                58,
                f"Current higher-study goal is {goal}; this path is strongest for {', '.join(criteria['goals'])}.",
                fit_notes,
                fit_blockers,
            )
        country_guidance = _country_guidance(preferred_country)
        ranked_universities = _rank_universities(recommendation.get("universities", []), preferred_country)
        if preferred_country and ranked_universities and UNIVERSITY_COUNTRIES.get(ranked_universities[0]) != preferred_country:
            fit_notes.append(f"No listed {preferred_country} university for this track; expand the country shortlist.")
        metrics = {
            "Best Higher Study Options": [recommendation["name"]],
            "Recommended Universities": ranked_universities,
            "Preferred Country": preferred_country or "Not specified",
            "Specialization Match": matched_interests[:4],
            "Research Readiness Score": round(_clamp(final_score), 2),
            "Entrance Exam Suggestions": _unique(recommendation.get("exams", []) + country_guidance["exams"]),
        }

        results.append(_result(
            recommendation,
            final_score,
            breakdown,
            strengths,
            missing,
            recommendation["next_steps"] + [country_guidance["next_step"]],
            metrics,
            fit_notes,
            fit_blockers,
            raw_score,
        ))

    return _package(level, results, limit)


def _package(level: dict[str, Any], results: list[dict[str, Any]], limit: int) -> dict[str, Any]:
    results.sort(key=lambda item: item["match_score"], reverse=True)
    top_results = results[:limit]
    average_score = round(sum(item["match_score"] for item in top_results) / len(top_results), 2) if top_results else 0
    confidence_counts: dict[str, int] = {}
    for item in top_results:
        label = item.get("confidence_label", "Unrated")
        confidence_counts[label] = confidence_counts.get(label, 0) + 1

    return {
        "academic_level": level["label"],
        "method_version": "rule-v2-fit-aware",
        "weights": level["weights"],
        "profile_summary": {
            "top_score": top_results[0]["match_score"] if top_results else 0,
            "average_top_score": average_score,
            "recommendation_count": len(top_results),
            "confidence_counts": confidence_counts,
        },
        "recommendations": top_results,
    }


def recommend_careers(
    assessment: dict[str, Any],
    dataset: dict[str, Any],
    limit: int = 5,
) -> dict[str, Any]:
    """Route an assessment to the correct level-specific scoring pipeline."""

    level_key = assessment.get("level_key") or normalize_level(assessment["academic_level"])
    levels = dataset.get("levels", {})
    level = levels.get(level_key)
    if not level:
        raise ValueError("No recommendation dataset is configured for this academic level.")

    data = assessment["data"]
    scorers = {
        "high_school": _score_high_school,
        "intermediate": _score_intermediate,
        "undergraduate": _score_undergraduate,
        "job_seeker": _score_job_seeker,
        "higher_studies": _score_higher_studies,
    }
    return scorers[level_key](data, level, limit)
