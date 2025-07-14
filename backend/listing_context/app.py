from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models import ListingModel
from ..fingerprint import compute_image_hash, compute_text_embedding
from ..common.db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ListingContext")


class ListingCreate(BaseModel):
    shop_url: str
    title: str
    description: str
    image_url: str


@app.post("/listings")
def create_listing(data: ListingCreate, db: Session = Depends(get_db)):
    image_hash = compute_image_hash(data.image_url)
    embedding = compute_text_embedding(data.description)
    listing = ListingModel(
        shop_url=data.shop_url,
        title=data.title,
        description=data.description,
        image_url=data.image_url,
        image_hash=image_hash,
        text_embedding=embedding,
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return {"id": str(listing.id)}


@app.get("/listings")
def list_listings(shop_url: str, db: Session = Depends(get_db)):
    listings = db.query(ListingModel).filter_by(shop_url=shop_url).all()
    return listings
