# Zomato v2: Restaurant & Menu Management API

## Overview
Zomato v2 is a FastAPI-based CRUD application that manages restaurants and their menu items, showcasing a one-to-many relationship using SQLAlchemy and SQLite.

- **Version 1**: Basic restaurant CRUD operations.
- **Version 2**: Extended with menu-item management and nested relationships.

## Features
- **Restaurant Endpoints**  
  - Create, read, update, delete restaurants  
  - Search restaurants by cuisine  
  - List only active restaurants  
- **Menu-Item Endpoints**  
  - Create, read, update, delete menu items  
  - Search menu items by category and dietary filters  
  - Nested endpoints to fetch restaurants with their menu and menu items with their restaurant details  
- **Database**: Async SQLite via SQLAlchemy  
- **Validation**: Pydantic v2 for request/response schemas  
- **Docs**: Interactive Swagger UI at `/docs`

## Prerequisites
- Python 3.8+  
- Git  
- pip (Python package manager)

## Setup Guide

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd zomato_v2
   ```

2. **Create & activate virtual environment**
   ```bash
   python3 -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```
   - Server runs on `http://127.0.0.1:8000`
   - Auto-generated docs: `http://127.0.0.1:8000/docs`

5. **Database initialization**
   - Tables are created automatically on startup.