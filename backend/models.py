from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(20), default="user") # "user" or "admin"
    free_generations_left = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("Session", back_populates="user")
    generations = relationship("VoiceGeneration", back_populates="user")
    downloads = relationship("Download", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    active_token = Column(String(500), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="sessions")

class VoiceGeneration(Base):
    __tablename__ = "voice_generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(Text)
    translated_text = Column(Text, nullable=True)
    language = Column(String(50))
    voice_type = Column(String(50)) # e.g., Male, Female, specific voice name
    file_path = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="generations")
    downloads = relationship("Download", back_populates="generation")

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    generation_id = Column(Integer, ForeignKey("voice_generations.id"))
    download_date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="downloads")
    generation = relationship("VoiceGeneration", back_populates="downloads")
