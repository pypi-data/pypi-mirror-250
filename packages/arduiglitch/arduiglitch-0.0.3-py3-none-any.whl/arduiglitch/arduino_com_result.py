"""
TypeAlias of two dataclasses to emulate the behaviour of Rust Result
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, Generic, TypeVar

T = TypeVar("T")

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err:
    value: Exception

Result: TypeAlias = Ok[T] | Err


