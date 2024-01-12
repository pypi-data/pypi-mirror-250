from datetime import date, datetime
from typing import (
    Annotated,
    Optional,
)

from pydantic import (
    Field,
    field_validator,
)

from .base import BaseUpdatableModel


class Tag(BaseUpdatableModel):
    """Tag"""

    author: Annotated[
        Optional[str],
        Field(validate_default=True, description="Author"),
    ] = None
    desc: Annotated[
        Optional[str],
        Field(repr=False, description="Description"),
    ] = None
    labels: Annotated[
        list[str],
        Field(default_factory=list, description="Labels"),
    ]
    vs: Annotated[
        Optional[date], Field(validate_default=True, alias="TagVersion")
    ] = None
    ts: Annotated[
        Optional[datetime],
        Field(validate_default=True, alias="TagTimestamp"),
    ] = None

    @field_validator("author")
    def set_author(cls, value: Optional[str]):
        return value or "undefined"

    @field_validator("vs")
    def set_version(cls, value: Optional[date]):
        """Pre initialize the `version` value that parsing from default"""
        return value if value else date(year=1990, month=1, day=1)

    @field_validator("ts")
    def set_ts(cls, value: Optional[datetime]):
        """Pre initialize the `ts` value that parsing from default"""
        return value or datetime.now()
