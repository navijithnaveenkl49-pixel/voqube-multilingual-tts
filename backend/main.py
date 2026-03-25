from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from fastapi.staticfiles import StaticFiles
import os, pathlib

import models, schemas, auth_utils, tts_service
from database import engine, get_db

# Ensure audio storage directory exists (needed on fresh Render deploys)
pathlib.Path("storage/audio").mkdir(parents=True, exist_ok=True)

# Create DB Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VoQube API", description="Multilingual TTS Generator SaaS", version="1.0.0")

# CORS Configuration
_frontend_url = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://voqube-multilingual-tts.vercel.app",
    "https://voqube-multilingual-tts.vercel.app/",
]
if _frontend_url:
    origins.append(_frontend_url)
    # Also add the URL with a trailing slash just in case
    origins.append(f"{_frontend_url}/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory to serve generated audio
app.mount("/static/audio", StaticFiles(directory="storage/audio"), name="audio")

@app.get("/")
def read_root():
    return {"message": "Welcome to VoQube API"}

# --- AUTHENTICATION ROUTES ---

@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="admin" if user.is_admin else "user",
        free_generations_left=10 if not user.is_admin else 9999
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    
    # Store session
    new_session = models.Session(user_id=user.id, active_token=access_token)
    db.add(new_session)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth_utils.get_current_active_user)):
    return current_user

# --- TTS CORE ROUTES ---

@app.post("/api/tts/generate", response_model=schemas.VoiceGenerationResponse)
async def generate_voice(request: schemas.VoiceGenerateRequest, 
                         current_user: models.User = Depends(auth_utils.get_current_active_user),
                         db: Session = Depends(get_db)):
    
    if current_user.free_generations_left <= 0 and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No free generations left. Please upgrade.")
    
    try:
        # 1. Translation
        if request.auto_translate:
            translated_text = await tts_service.translate_text(request.text, request.language)
        else:
            translated_text = request.text
        
        file_path = await tts_service.generate_speech(
            text=translated_text,
            language=request.language,
            voice_type=request.voice or request.voice_type
        )
        
        # Determine accessible path since it's mounted
        # storage/audio/...mp3 -> /static/audio/...mp3
        public_path = "/static/audio/" + file_path.split("/")[-1].split("\\")[-1]

        # Save to DB
        generation = models.VoiceGeneration(
            user_id=current_user.id,
            text=request.text,
            translated_text=translated_text if request.language != "English" else None,
            language=request.language,
            voice_type=request.voice_type,
            file_path=public_path
        )
        db.add(generation)
        
        if current_user.role != "admin":
            current_user.free_generations_left -= 1
            
        db.commit()
        db.refresh(generation)
        
        return generation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-voice")
async def generate_voice_explicit(request: schemas.VoiceGenerateRequest, 
                               db: Session = Depends(get_db)):
    """
    Direct endpoint for voice generation as requested.
    Uses Edge-TTS for high-quality Malayalam neural voices.
    """
    try:
        # 1. Translation
        if request.auto_translate:
            translated_text = await tts_service.translate_text(request.text, request.language)
        else:
            translated_text = request.text
        
        # 2. Generation using translated text
        file_path = await tts_service.generate_speech(
            text=translated_text,
            language=request.language,
            voice_type=request.voice or request.voice_type
        )
        
        # Determine accessible path
        public_path = "/static/audio/" + file_path.split("/")[-1].split("\\")[-1]
        
        return {
            "file_path": public_path, 
            "translated_text": translated_text if request.language != "English" else None,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tts/history", response_model=List[schemas.VoiceGenerationResponse])
def get_user_history(current_user: models.User = Depends(auth_utils.get_current_active_user),
                     db: Session = Depends(get_db)):
    history = db.query(models.VoiceGeneration).filter(
        models.VoiceGeneration.user_id == current_user.id,
        models.VoiceGeneration.is_deleted == False
    ).order_by(models.VoiceGeneration.created_at.desc()).all()
    return history

@app.post("/api/tts/history/{generation_id}/trash")
def move_to_trash(generation_id: int, 
                  current_user: models.User = Depends(auth_utils.get_current_active_user),
                  db: Session = Depends(get_db)):
    generation = db.query(models.VoiceGeneration).filter(
        models.VoiceGeneration.id == generation_id, 
        models.VoiceGeneration.user_id == current_user.id
    ).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
        
    generation.is_deleted = True
    db.commit()
    return {"status": "moved to trash"}

@app.get("/api/tts/trash", response_model=List[schemas.VoiceGenerationResponse])
def get_trash(current_user: models.User = Depends(auth_utils.get_current_active_user),
              db: Session = Depends(get_db)):
    trashed = db.query(models.VoiceGeneration).filter(
        models.VoiceGeneration.user_id == current_user.id,
        models.VoiceGeneration.is_deleted == True
    ).order_by(models.VoiceGeneration.created_at.desc()).all()
    return trashed

@app.post("/api/tts/trash/{generation_id}/restore")
def restore_from_trash(generation_id: int, 
                       current_user: models.User = Depends(auth_utils.get_current_active_user),
                       db: Session = Depends(get_db)):
    generation = db.query(models.VoiceGeneration).filter(
        models.VoiceGeneration.id == generation_id, 
        models.VoiceGeneration.user_id == current_user.id
    ).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
        
    generation.is_deleted = False
    db.commit()
    return {"status": "restored"}

@app.delete("/api/tts/trash/{generation_id}")
def delete_permanently(generation_id: int, 
                       current_user: models.User = Depends(auth_utils.get_current_active_user),
                       db: Session = Depends(get_db)):
    generation = db.query(models.VoiceGeneration).filter(
        models.VoiceGeneration.id == generation_id, 
        models.VoiceGeneration.user_id == current_user.id
    ).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
        
    db.delete(generation)
    db.commit()
    return {"status": "deleted permanently"}

@app.post("/api/tts/track_download/{generation_id}")
def track_download(generation_id: int, 
                   current_user: models.User = Depends(auth_utils.get_current_active_user),
                   db: Session = Depends(get_db)):
    generation = db.query(models.VoiceGeneration).filter(models.VoiceGeneration.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
        
    download = models.Download(user_id=current_user.id, generation_id=generation.id)
    db.add(download)
    db.commit()
    return {"status": "success"}

# --- ADMIN ROUTES ---

@app.get("/api/admin/users", response_model=List[schemas.UserResponse])
def get_all_users(current_admin: models.User = Depends(auth_utils.get_current_admin_user),
                  db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/api/admin/stats")
def get_system_stats(current_admin: models.User = Depends(auth_utils.get_current_admin_user),
                     db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    total_generations = db.query(models.VoiceGeneration).count()
    total_downloads = db.query(models.Download).count()
    
    return {
        "total_users": total_users,
        "total_generations": total_generations,
        "total_downloads": total_downloads
    }

@app.put("/api/admin/users/{user_id}/tokens", response_model=schemas.UserResponse)
def update_user_tokens(user_id: int, 
                       token_data: schemas.TokenUpdate,
                       current_admin: models.User = Depends(auth_utils.get_current_admin_user),
                       db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.free_generations_left = token_data.tokens
    db.commit()
    db.refresh(user)
    return user

@app.get("/api/admin/generations", response_model=List[schemas.AdminVoiceGenerationResponse])
def get_all_generations_admin(current_admin: models.User = Depends(auth_utils.get_current_admin_user),
                              db: Session = Depends(get_db)):
    generations = db.query(models.VoiceGeneration).order_by(models.VoiceGeneration.created_at.desc()).all()
    return generations
