from dataclasses import dataclass, field
from typing import Literal


@dataclass(kw_only=True)
class Failure:
    duration: float | None
    error: Exception
    type: Literal["failure"] = field(default="failure")


@dataclass(kw_only=True)
class Skip:
    message: str
    type: Literal["skip"] = field(default="skip")


@dataclass(kw_only=True)
class Success:
    duration: float
    type: Literal["success"] = field(default="success")
