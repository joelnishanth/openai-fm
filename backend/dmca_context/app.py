from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models import ViolationModel, ListingModel
from ..fingerprint import _json_rpc
from ..common.db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DMCAContext")


class GenerateRequest(BaseModel):
    violation_id: str


@app.post("/generate")
def generate_dmca(req: GenerateRequest, db: Session = Depends(get_db)):
    violation = db.query(ViolationModel).filter_by(id=req.violation_id).first()
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    listing = db.query(ListingModel).filter_by(id=violation.original_listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    prompt = (
        f"Draft a formal DMCA takedown notice.\n"
        f"My original listing is titled '{listing.title}' at {listing.shop_url}.\n"
        f"The violating listing is located at {violation.suspect_url}."
    )
    result = _json_rpc("generate", {"model": "llama3", "prompt": prompt})
    return {"notice": result}
