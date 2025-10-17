from fastapi import FastAPI, HTTPException
from typing import Optional
import uvicorn

app = FastAPI(
    title="Parameters and Exceptions API",
    description="An example API to demonstrate Path & Query parameters and HTTPException.",
)

# A simple in-memory "database" of an inventory
inventory_db = {
    1: {"name": "Laptop", "category": "Electronics"},
    2: {"name": "Desk Chair", "category": "Furniture"},
    3: {"name": "Coffee Mug", "category": "Kitchenware"},
}

# --- 1. A friendly root endpoint ---
@app.get("/")
def read_root():
    return {
        "message": "Welcome!",
        "instructions": "Try accessing /items/{item_id} with optional query parameters."
    }


# --- 2. Endpoint combining all concepts ---
@app.get("/items/{item_id}")
def get_item_details(item_id: int, brand: Optional[str] = None, show_category: bool = True):
    """
    Retrieves an item from the inventory.

    - **item_id** (Path Parameter): The unique ID of the item. Required.
    - **brand** (Query Parameter): The brand name of the item. Optional.
    - **show_category** (Query Parameter): Set to false to hide the category. Optional.
    """

    # --- HTTPException Handling ---
    # Check if the item_id from the path exists in our database.
    # If not, we raise an HTTPException with a 404 status code.
    if item_id not in inventory_db:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} could not be found."
        )

    # If we find the item, get its data
    item = inventory_db[item_id]
    response_data = {"id": item_id, "name": item["name"]}

    # --- Query Parameter Logic ---
    # Add the brand to the response only if the client provided it
    if brand:
        response_data["brand"] = brand

    # Include the category based on the boolean query parameter
    if show_category:
        response_data["category"] = item["category"]

    return response_data

# --- 3. How to Run This App ---
#
#    uvicorn parameters_and_exceptions_api:app --reload
#
#    Then, open your browser and test these URLs:
#    - http://127.0.0.1:8000/items/1                  (Success)
#    - http://127.0.0.1:8000/items/2?brand=ErgoMax    (Success with query param)
#    - http://127.0.0.1:8000/items/3?show_category=false (Success with another query param)
#    - http://127.0.0.1:8000/items/99                 (Triggers 404 HTTPException)
