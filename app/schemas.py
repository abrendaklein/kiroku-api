from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class KirokuCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class KirokuUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None

    model_config = ConfigDict(extra="forbid")

    # title and completed are required in the db, so null is rejected (422)
    @field_validator("title", "completed", mode="before")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("this field cannot be null")
        return value


class KirokuResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)