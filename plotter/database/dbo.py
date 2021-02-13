"""Database object definitions"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PointDBO:
    x_value: int
    y_value: int


@dataclass
class PointListDBO:
    inserted_at: Optional[int]
    points: list[PointDBO]
