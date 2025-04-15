from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import users, crops, diseases
from utils.auth import get_current_user

app = FastAPI(
    title="Agric-Advisor API",
    description="An agricultural advisory system API",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@agricadvisor.com"
    },
    license_info={
        "name": "MIT",
    },
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with tags and descriptions
app.include_router(
    users.router,
    tags=["Authentication"],
    prefix="/auth"
)
app.include_router(
    crops.router,
    tags=["Crops"],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    diseases.router,
    tags=["Diseases"],
    responses={404: {"description": "Not found"}}
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agric-Advisor API"}

@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": user.username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
