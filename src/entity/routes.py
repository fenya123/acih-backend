"""Routes for Entity package."""

from __future__ import annotations

from fastapi import APIRouter

from src.entity.models import Entity
from src.entity.schemas import EntitiesSchema, EntitySchema
from src.shared.database import Db


router = APIRouter()


@router.post("/entities/{entity_id}")
def create_entity(entity_id: int, db: Db) -> EntitySchema:
    """Create a new entity."""
    new_entity = Entity(id=entity_id)
    db.add(new_entity)
    db.commit()
    return EntitySchema.from_orm(new_entity)


@router.get("/entities")
def get_entity_list(db: Db) -> EntitiesSchema:
    """Get list of entities."""
    entities = db.query(Entity).all()
    return EntitiesSchema(entities=entities)
