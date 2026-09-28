from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request},
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request},
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request},
    )


@router.get("/planner/{planner_type}", response_class=HTMLResponse)
def planner(request: Request, planner_type: str):
    if planner_type not in {"home", "party", "jewelry"}:
        planner_type = "home"

    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={
            "request": request,
            "planner": planner_type,
        },
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"request": request},
    )