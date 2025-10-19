import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic models
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


# In-memory storage for demo (replace with database in real app)
items_db = []
next_id = 1


@router.get("/items", response_model=list[ItemResponse])
async def list_items(db: AsyncSession | None = Depends(get_database)):
    """List all items."""
    logger.info("Listing all items")
    return items_db


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, db: AsyncSession | None = Depends(get_database)):
    """Create a new item."""
    global next_id

    new_item = ItemResponse(
        id=next_id,
        name=item.name,
        description=item.description,
        price=item.price,
    )

    items_db.append(new_item)
    next_id += 1

    logger.info(f"Created item: {new_item.name}")
    return new_item


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession | None = Depends(get_database)):
    """Get a specific item by ID."""
    for item in items_db:
        if item.id == item_id:
            logger.info(f"Retrieved item: {item.name}")
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession | None = Depends(get_database),
):
    """Update an existing item."""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            # Update fields if provided
            if item_update.name is not None:
                item.name = item_update.name
            if item_update.description is not None:
                item.description = item_update.description
            if item_update.price is not None:
                item.price = item_update.price

            logger.info(f"Updated item: {item.name}")
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession | None = Depends(get_database)):
    """Delete an item."""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            logger.info(f"Deleted item: {deleted_item.name}")
            return {"message": "Item deleted successfully"}

    raise HTTPException(status_code=404, detail="Item not found")
