from fastapi import FastAPI
from routers import auth,dash_summary,zones,admin,sos_request
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],        
)
app.include_router(auth.router)
app.include_router(dash_summary.router)
app.include_router(zones.router)
app.include_router(admin.router)
app.include_router(sos_request.router)