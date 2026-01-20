# 🛒 Full Stack E-Commerce Application

A high-performance E-Commerce platform built with **FastAPI** (Backend) and **React.js** (Frontend).

## 🚀 Features
- **JWT Authentication:** Secure user login and registration.
- **Product Management:** Create, read, and manage product inventory.
- **Order System:** Atomic transactions ensure stock is deducted correctly when orders are placed.
- **Inventory Management:** Prevents overselling products.
- **Role-Based Isolation:** Users can only view their own orders.
- **Interactive UI:** React Frontend connected to the backend via Axios.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy (SQLite), Pydantic.
- **Frontend:** React.js, Axios.
- **Security:** OAuth2 with Password (JWT), Passlib (Bcrypt hashing).
- **Database:** SQLite (SQLAlchemy ORM).

## ⚙️ Installation & Setup

### 1. Backend Setup (FastAPI)
Make sure you have Python installed.

```bash
# Navigate to the root directory
cd app

# Install dependencies (Create a requirements.txt if you haven't)
pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography] python-multipart

# Start the Server
uvicorn main:app --reload
The Backend will run at: http://127.0.0.1:8000 API Documentation (Swagger UI): http://127.0.0.1:8000/docs


# start the frontend
# Navigate to the frontend directory
cd frontend

# Install libraries
npm install

# Start the React App
npm start

port 3000
The Frontend will run at: http://localhost:3000


# Folder Structure
e-commerce/
├── app/                  # FastAPI Backend
│   ├── routers/          # API Endpoints (users, products, orders, auth)
│   ├── models/           # Database Tables (SQLAlchemy)
│   ├── schemas/          # Pydantic Models (Validation)
│   ├── main.py           # Entry point
│   └── database.py       # DB Connection
├── frontend/             # React Frontend
│   ├── src/              # React Components (App.js, Login.js)
│   └── public/           # Static assets
└── README.md             # Project Documentation

Once you save this file, your VS Code "Source Control" tab will show `README.md` as a new file (U - Untracked).

Run these commands in your terminal to send it to GitHub:

```powershell
git add .
git commit -m "Added documentation"
git push