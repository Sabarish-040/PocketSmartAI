import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Recommendation, User
from app.schemas import (
    HomeRequest,
    PartyRequest,
    RecommendationResponse,
)
from app.services.planner_service import (
    build_home_plan,
    build_jewelry_plan,
    build_party_plan,
)

router = APIRouter(
    prefix="/api",
    tags=["Planners"],
)


@router.post(
    "/planner/home",
    response_model=RecommendationResponse,
)
def home_planner(
    payload: HomeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = build_home_plan(
        payload.budget,
        payload.room,
        payload.style,
        payload.items,
    )

    db.add(
        Recommendation(
            user_id=user.id,
            planner_type="home",
            request_json=payload.model_dump_json(),
            response_json=json.dumps(result),
        )
    )

    db.commit()

    return result


@router.post(
    "/planner/party",
    response_model=RecommendationResponse,
)
def party_planner(
    payload: PartyRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = build_party_plan(
        payload.budget,
        payload.guests,
        payload.event_type,
        payload.venue,
    )

    db.add(
        Recommendation(
            user_id=user.id,
            planner_type="party",
            request_json=payload.model_dump_json(),
            response_json=json.dumps(result),
        )
    )

    db.commit()

    return result


@router.post("/planner/jewelry")
def jewelry_planner(
    payload: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    budget = float(payload.get("budget", 0))

    result = build_jewelry_plan(budget)

    db.add(
        Recommendation(
            user_id=user.id,
            planner_type="jewelry",
            request_json=json.dumps(payload),
            response_json=json.dumps(result),
        )
    )

    db.commit()

    return result


@router.get("/history")
def recommendation_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "planner_type": item.planner_type,
            "request": json.loads(item.request_json),
            "response": json.loads(item.response_json),
            "created_at": item.created_at.isoformat(),
        }
        for item in records
    ]