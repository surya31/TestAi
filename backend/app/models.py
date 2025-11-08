"""Pydantic models used across the Emotional Companion backend."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class EmotionLabel(str, Enum):
    """Enumerate a baseline set of supported emotions."""

    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    CALM = "calm"
    LOVE = "love"


class JournalEntryBase(BaseModel):
    content: str = Field(..., description="Free-form journaling content")
    emotion: EmotionLabel = Field(..., description="Dominant emotion during the entry")
    tags: List[str] = Field(default_factory=list, description="User-defined tags")
    attachments: List[str] = Field(
        default_factory=list,
        description="Optional URIs for audio, video, or other supporting files.",
    )


class JournalEntryCreate(JournalEntryBase):
    entry_id: Optional[str] = Field(
        default=None,
        description="Client-provided identifier. If omitted, the server generates one.",
    )


class JournalEntryRead(JournalEntryBase):
    entry_id: str
    created_at: datetime

    class Config:
        json_encoders = {datetime: lambda value: value.isoformat()}


__all__ = [
    "EmotionLabel",
    "JournalEntryBase",
    "JournalEntryCreate",
    "JournalEntryRead",
]
