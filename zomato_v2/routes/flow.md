Client
  ↓ HTTP request
uvicorn → FastAPI
  ↓ route dispatch
routes/*.py
  ↓ input validation (Pydantic schemas)
schemas.py (input models)
  ↓ business logic call
crud.py
  ↓ ORM/database operations
database.py & models.py
  ↑ returns ORM objects
routes/*.py
  ↓ output validation & serialization
schemas.py (response models)
  ↓ JSON response
Client