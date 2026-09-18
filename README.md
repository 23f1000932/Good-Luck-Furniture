# Good Luck Furniture

## Project Structure

```
Good-Luck-Furniture/
├── backend/          # Flask REST API
├── frontend/         # Vue 3 + Vite frontend
├── .gitignore
└── README.md
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Initialize database
flask db init
flask db migrate -m "initial"
flask db upgrade

# Seed default categories
flask seed-categories

# Create admin user
flask seed-admin

# Run development server
python run.py
```

Backend runs at: http://localhost:5000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## Business Information

- **Address:** Opposite Sai Dham Apartments, Rehmat Complex, Rajrooppur, Prayagraj, Uttar Pradesh 211015
- **Phone:** 9415612726
- **Email:** abadhussain4212@gmail.com
- **Hours:** 11 AM – 9 PM

## Tech Stack

- **Frontend:** Vue 3 + Vite + Vue Router + Pinia
- **Backend:** Python + Flask + Flask-SQLAlchemy + Flask-JWT-Extended
- **Dev DB:** SQLite
- **Prod DB:** PostgreSQL (Supabase)
- **Dev Images:** Local filesystem (`backend/uploads/`)
- **Prod Images:** Supabase Storage
