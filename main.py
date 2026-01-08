from fastapi import FastAPI
from routers import auth,dash_summary,zones
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],        # <-- IMPORTANT
    allow_headers=["*"],        # <-- IMPORTANT
)
app.include_router(auth.router)
app.include_router(dash_summary.router)
app.include_router(zones.router)