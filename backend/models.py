from sqlalchemy import Column, String, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .common.db import Base


class ListingModel(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    image_hash = Column(String, nullable=False)
    text_embedding = Column(ARRAY(Float))
    created_at = Column(DateTime, default=datetime.utcnow)


class ViolationModel(Base):
    __tablename__ = "violations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_listing_id = Column(UUID(as_uuid=True))
    suspect_url = Column(String, nullable=False)
    suspect_image_url = Column(String)
    similarity_score = Column(Float)
    platform = Column(String, default="etsy")
    reported = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
