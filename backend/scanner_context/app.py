from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from ..models import ListingModel, ViolationModel
from ..fingerprint import compare_embeddings, compare_image_hashes
from ..common.db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScannerContext")


class ScanRequest(BaseModel):
    shop_url: str


@app.post("/scan")
def scan_listings(data: ScanRequest, db: Session = Depends(get_db)):
    listings = db.query(ListingModel).filter_by(shop_url=data.shop_url).all()
    violations: List[ViolationModel] = []
    # simulate suspect listings by comparing within same listings
    for i, l1 in enumerate(listings):
        for l2 in listings[i + 1 :]:
            emb_score = compare_embeddings(l1.text_embedding, l2.text_embedding)
            img_score = compare_image_hashes(l1.image_hash, l2.image_hash)
            score = max(emb_score, img_score)
            if score > 0.85:
                violation = ViolationModel(
                    original_listing_id=l1.id,
                    suspect_url=l2.shop_url,
                    suspect_image_url=l2.image_url,
                    similarity_score=score,
                )
                db.add(violation)
                violations.append(violation)
    db.commit()
    return [{"id": str(v.id), "score": v.similarity_score} for v in violations]
