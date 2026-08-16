from core.crud import crud_router


router = crud_router(
    "/apps",
    "Apps",
    "apps",
    response_key="app",
    payload_key="data",
)
