# Food Menu Management API

A simple FastAPI application for managing a restaurant's food menu. Staff can add, update, and delete menu items; customers can browse and filter by category.

## Features

* Define menu items with validation via Pydantic models.
* In-memory data store (`menu_db`) for fast prototyping.
* CRUD endpoints for menu items.
* Category-based filtering.
* Stubbed authentication for staff-only operations.

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn (ASGI server)
* Pydantic

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/food-menu-api.git
   cd food-menu-api
   ```

2. **Create a virtual environment and activate it**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn
   ```

## Running the App

Start the development server with Uvicorn:

```bash
uvicorn main:app --reload
```

* The API will be available at `http://127.0.0.1:8000`.
* Interactive API docs:

  * Swagger UI: `http://127.0.0.1:8000/docs`
  * ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Path                        | Description                         |
| ------ | --------------------------- | ----------------------------------- |
| GET    | `/menu`                     | List all menu items                 |
| GET    | `/menu/{item_id}`           | Retrieve details of a specific item |
| POST   | `/menu`                     | Create a new menu item (staff only) |
| PUT    | `/menu/{item_id}`           | Update an existing menu item        |
| DELETE | `/menu/{item_id}`           | Delete a menu item                  |
| GET    | `/menu/category/{category}` | List items by category              |

### Sample Request and Response

**Create a new item**

```http
POST /menu HTTP/1.1
Content-Type: application/json

{
  "name": "Margherita Pizza",
  "description": "Classic pizza with fresh tomatoes and mozzarella cheese.",
  "category": "main_course",
  "price": 12.99,
  "preparation_time": 15,
  "ingredients": ["flour", "tomato", "mozzarella", "basil"],
  "calories": 800,
  "is_vegetarian": true,
  "is_spicy": false
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Margherita Pizza",
  "description": "Classic pizza with fresh tomatoes and mozzarella cheese.",
  "category": "main_course",
  "price": 12.99,
  "is_available": true,
  "preparation_time": 15,
  "ingredients": ["flour", "tomato", "mozzarella", "basil"],
  "calories": 800,
  "is_vegetarian": true,
  "is_spicy": false
}
```

## Authentication Stub

* The `POST`, `PUT`, and `DELETE` endpoints depend on a stubbed `get_current_staff_user()` that always grants access. Replace with real auth logic as needed.