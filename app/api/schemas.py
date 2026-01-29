from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class DocumentRead(BaseModel):
    id: int
    title: str
    source: Optional[str]
    status: str
    quality_score: Optional[float]

    class Config:
        from_attributes = True


class ChunkRead(BaseModel):
    id: int
    document_id: int
    content: str
    quality_score: Optional[float]
    status: str

    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    question: str
    metadata: Optional[dict[str, Any]] = None


class QueryRead(BaseModel):
    id: int
    question: str
    answer: Optional[str]
    success: bool
    confidence: Optional[float]
    entropy: Optional[float]
    failure_mode: Optional[str]

    class Config:
        from_attributes = True


class MetricRead(BaseModel):
    id: int
    name: str
    value: float
    window: str
    created_at: datetime

    class Config:
        from_attributes = True


class LearningRunResponse(BaseModel):
    status: str = Field(..., description="Status of learning cycle execution")


class TopicsResponse(BaseModel):
    topics: list[str]


class SyntheticQARead(BaseModel):
    id: int
    question: str
    answer: str
    topic: Optional[str]
    qa_type: Optional[str]
    quality_score: Optional[float]

    class Config:
        from_attributes = True

