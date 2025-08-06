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
   cd zomato_v1
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
   - The SQLite file `restaurants.db` is generated in the project root.

## Project Structure
```
zomato_v1/
├── main.py                  # Application entrypoint and router mounting
├── database.py              # Async engine, session factory, table creation
├── models.py                # SQLAlchemy ORM definitions for Restaurant & MenuItem
├── schemas.py               # Pydantic schemas for validation & nested models
├── crud.py                  # Data-access functions for Restaurant & MenuItem
├── requirements.txt         # Pinned Python dependencies
├── restaurants.db           # SQLite database file (auto-generated)
└── routes/
    ├── restaurants.py       # `/restaurants` and nested menu routes
    └── menu_items.py        # `/menu-items` standalone routes
```

## API Endpoints

### Restaurants
| Method | Path                                  | Description                                      |
| ------ | ------------------------------------- | ------------------------------------------------ |
| POST   | `/restaurants/`                       | Create a new restaurant                          |
| GET    | `/restaurants/`                       | List restaurants (`skip`, `limit` query params)  |
| GET    | `/restaurants/{restaurant_id}`        | Get a single restaurant                          |
| PUT    | `/restaurants/{restaurant_id}`        | Update a restaurant                              |
| DELETE | `/restaurants/{restaurant_id}`        | Delete a restaurant                              |
| GET    | `/restaurants/search?cuisine=…`       | Search by cuisine                                |
| GET    | `/restaurants/active`                 | List only active restaurants                     |
| POST   | `/restaurants/{id}/menu-items/`       | Add a menu item to a restaurant                  |
| GET    | `/restaurants/{id}/menu`              | List menu items for a restaurant                 |
| GET    | `/restaurants/{id}/with-menu`         | Get restaurant with its full menu                |

### Menu Items
| Method | Path                                           | Description                                      |
| ------ | ---------------------------------------------- | ------------------------------------------------ |
| GET    | `/menu-items/`                                 | List all menu items (`skip`, `limit`)            |
| GET    | `/menu-items/{item_id}`                        | Get a single menu item                           |
| GET    | `/menu-items/{item_id}/with-restaurant`        | Get menu item with parent restaurant details     |
| PUT    | `/menu-items/{item_id}`                        | Update a menu item                               |
| DELETE | `/menu-items/{item_id}`                        | Delete a menu item                               |
| GET    | `/menu-items/search?category=&vegetarian=&vegan=` | Search with filters (category, vegetarian, vegan)|

## Contributing
1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/name`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to branch (`git push origin feature/name`)  
5. Open a Pull Request

## License
MIT License
