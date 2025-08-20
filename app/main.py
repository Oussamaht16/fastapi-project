from . import models
from .database import engine
from fastapi import FastAPI
from .routers import post, user, auth, vote
from .config import settings

# CROS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine).....
# 9alk madam rana nyusiw alembic ||models.Base.metadata.create_all(bind=engine)|| maeadna mandiro


# hada howa sah li t9dr tactivi bih les request mn les file wakhdokhrin
app = FastAPI()
# CORS origins hadi rah tkon list dyal les origins ... 
origins = ["http://localhost:3000"]
""" #🔐 ملاحظة أمنية مهمة:
لا تضع مواقع مثل google.com أو facebook.com في origins في مشروعك الحقيقي!!
هذه التجربة فقط لأغراض تعليمية. لأنه في المشروع الحقيقي:

يجب أن تسمح فقط لتطبيقك الأمامي (مثلاً: "https://easyrideplus.dz") بالوصول إلى الـ Back-End. """


# CROS hado jbnahom mn docs cros fastapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
