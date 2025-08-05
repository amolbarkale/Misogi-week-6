# Restaurant Ordering System

A simple FastAPI application for managing a restaurant’s menu and customer orders, using Pydantic models and in-memory storage.

## Features

* **Menu Management**

  * Create, read, update, and delete food items
  * Filter items by category
* **Order Management**

  * Place orders with nested customer and item details
  * List orders (summary and detailed views)
  * Update order status
* **Validation & Computation**

  * Pydantic schemas enforce data rules
  * Computed properties for item totals and order totals
* **Authentication Stub**

  * Staff-only endpoints protected by a simple dependency (replace with real auth)

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic

## Project Structure

```
restaurant-ordering-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── dependencies.py
│   └── routers/
│       ├── menu.py
│       └── orders.py
├── requirements.txt
└── README.md
```

## Prerequisites

* Python 3.10 or higher
* pip (Python package installer)

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd restaurant-ordering-system
   ```
2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\\Scripts\\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

* The API will be available at `http://127.0.0.1:8000`.
* Interactive API docs:

  * Swagger UI: `http://127.0.0.1:8000/docs`
  * ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Menu Endpoints

| Method | Path                        | Description                         |
| ------ | --------------------------- | ----------------------------------- |
| GET    | `/menu`                     | List all menu items                 |
| GET    | `/menu/{item_id}`           | Get details for a specific item     |
| POST   | `/menu`                     | Create a new menu item (staff only) |
| PUT    | `/menu/{item_id}`           | Update an existing menu item        |
| DELETE | `/menu/{item_id}`           | Delete a menu item (staff only)     |
| GET    | `/menu/category/{category}` | List items by category              |

### Orders Endpoints

| Method | Path                        | Description                            |
| ------ | --------------------------- | -------------------------------------- |
| POST   | `/orders`                   | Create a new order                     |
| GET    | `/orders`                   | List all orders (summary view)         |
| GET    | `/orders/{order_id}`        | Get detailed order info                |
| PUT    | `/orders/{order_id}/status` | Update the status of an existing order |

## Models / Schemas

* **FoodItemBase**: Request schema for menu items
* **FoodItem**: Response schema including `id`
* **OrderItem**, **Customer**, **Order**, **OrderSummary**, **StatusUpdate**

## Authentication

* The `POST`, `PUT`, and `DELETE` endpoints require a staff check via `get_current_staff_user()` in `app/dependencies.py`.
