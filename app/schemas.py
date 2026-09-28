from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    room: str = Field(min_length=2, max_length=80)
    style: str = Field(
        default="modern",
        min_length=2,
        max_length=80,
    )
    items: str = Field(
        default="lights, ceiling fan, decor",
        max_length=500,
    )


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(
        default="flexible",
        max_length=120,
    )


class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: float
    platform: str
    url: str
    reason: str


class RecommendationResponse(BaseModel):
    planner: str
    budget: float
    summary: str
    allocation: dict[str, float]
    recommendations: list[RecommendationItem]
    disclaimer: str
    source: str


class SessionInfo(BaseModel):
    authenticated: bool
    user_id: int | None = None
    name: str | None = None
    email: str | None = None