from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    free_generations_left: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class VoiceGenerateRequest(BaseModel):
    text: str
    language: str
    voice_type: Optional[str] = "Female"
    voice: Optional[str] = None
    auto_translate: Optional[bool] = True

class VoiceGenerationResponse(BaseModel):
    id: int
    text: str
    translated_text: Optional[str] = None
    language: str
    voice_type: str
    file_path: str
    is_deleted: Optional[bool] = False
    created_at: datetime

    class Config:
        orm_mode = True

class DownloadRecordResponse(BaseModel):
    id: int
    user_id: int
    generation_id: int
    download_date: datetime
    
    class Config:
        orm_mode = True

class TokenUpdate(BaseModel):
    tokens: int

class AdminVoiceGenerationResponse(VoiceGenerationResponse):
    user_id: int
    user: UserResponse
