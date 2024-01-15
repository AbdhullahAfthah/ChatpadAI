from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import shutil
import os
from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils import *
from typing import Optional


SECRET_KEY = "1b3179db99127758e570f9af2f3ba5eeb7b7084115818255c3eaec4becc89301"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:5500",  # Add your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ... your route handlers go here ...

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# changed to hashed_password
def get_password_hash(hashed_password):
    return pwd_context.hash(hashed_password)

def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    print(user)
    return user

    
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user
    

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(current_user: schemas.UserCreate = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user



@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# who signed in
@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: models.User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]



@app.post("/create_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/upload-pdf/")
# async def upload_pdf(
#     token: str = Depends(oauth2_scheme),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     try:
#         user_info = await get_current_user(token, db)
#         user_id = user_info.id

#         upload_dir = "sql_app/uploads"
#         os.makedirs(upload_dir, exist_ok=True)
#         file_extension = file.filename.split(".")[-1]
#         random_filename = generate_random_filename(file_extension)\
        
#         file_path = os.path.join(upload_dir, random_filename)

#         with open(file_path, "wb") as new_file:
#             shutil.copyfileobj(file.file, new_file)

#         resource_id = crud.create_resource(db=db, user_id=user_id, file_path=file_path)

#         absolute_file_path = os.path.abspath(file_path)

#         return JSONResponse(content={
#             "message": "File uploaded successfully",
#             "resource_id": resource_id,
#             "file_path": absolute_file_path,
#             "filename": random_filename
#             }, status_code=200)

#     except Exception as e:
#         return JSONResponse(content={"message": "Error uploading file", "error": str(e)}, status_code=500)
    

@app.post("/upload-pdf/")
async def upload_pdf(
    token: str = Depends(oauth2_scheme),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        user_info = await get_current_user(token, db)
        user_id = user_info.id

        upload_dir = "sql_app/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = file.filename.split(".")[-1]
        random_filename = generate_random_filename(file_extension)
        file_path = os.path.join(upload_dir, random_filename)

        with open(file_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # Save to the database
        resource_id = crud.create_resource(db=db, user_id=user_id, file_path=file_path)

        # Copy to frontend folder
        frontend_folder = Path(__file__).parent.parent.parent / "ChatpadAI" / "frontend" / "hostit-html" / "pdfs"
        frontend_file_path = frontend_folder / file.filename
        shutil.copy(file_path, frontend_file_path)

        absolute_file_path = os.path.abspath(file_path)

        return JSONResponse(content={
            "message": "File uploaded successfully",
            "resource_id": resource_id,
            "filename": random_filename,
            "file_path": absolute_file_path,
        }, status_code=200)

    except HTTPException as e:
        return JSONResponse(content={"message": f"Error uploading file - {e.detail}", "error": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading file", "error": str(e)}, status_code=500)





@app.post("/upload-url/")
async def upload_url(
    url_data: schemas.URLData,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        user_info = await get_current_user(token, db)
        user_id = user_info.id

        resource_id = crud.create_resource_url(db=db, user_id=user_id, url=url_data.url)

        return JSONResponse(content={
            "message": "URL uploaded successfully",
            "resource_id": resource_id,
            "url": url_data.url, 
        }, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": "Error uploading URL", "error": str(e)}, status_code=500)