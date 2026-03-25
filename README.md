# VoQube - Multilingual TTS Generator

VoQube is a modern, high-performance Text-to-Speech (TTS) generator designed for gamers, streamers, and content creators. It supports multiple languages and provides a sleek dashboard for managing voice generations.

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+**
- **Node.js 18+**
- **MySQL 8.0+**

### Backend Setup
1. Navigate to the `backend` folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `.env` with your MySQL credentials.
5. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup
1. Navigate to the `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 🔑 Access Credentials

### Administrator
- **Username**: `admin`
- **Password**: `admin123`
- **Features**: Full access to Admin Panel, user management, and unlimited voice generations.

### Standard User
- **Username**: `demouser456`
- **Password**: `password123`
- **Features**: Dashboard access with a limited token balance (10 tokens by default).

## ✨ Features
- **Multilingual Support**: Generate speech in various Indian and international languages.
- **Voice Selection**: Choose between different voice types (Male/Female).
- **Admin Control**: Administrators can manually update user token balances from the Admin Panel.
- **Generation History**: Track and download previous voice generations.
- **Sleek UI**: Built with React and Material UI for a premium, responsive experience.

## 🛠️ Tech Stack
- **Frontend**: React, Vite, Material UI (MUI)
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: MySQL
- **Audio Service**: gTTS (Google Text-to-Speech) / Edge-TTS
