# 🛡️ AI-Powered Coupon Fraud Detection System

A full-stack, microservices-based fraud detection system that identifies and prevents coupon abuse in real-time.

## 🏗️ Architecture

- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **Backend:** Django REST Framework + PostgreSQL
- **ML Service:** FastAPI + Rule-based AI
- **Deployment:** Vercel (Frontend) + Render (Backend/ML)

## 🚀 Features

- Real-time fraud scoring using AI rules
- Beautiful responsive dashboard
- Admin panel for transaction monitoring
- RESTful API architecture
- Redis caching for performance

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/your-username/fraud-detection-project.git

# Setup backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

# Setup ML service  
cd ../ml-service && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Setup frontend
cd ../frontend && npm install
npm run dev