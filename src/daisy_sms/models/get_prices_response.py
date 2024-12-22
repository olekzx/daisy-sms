from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceDetails:
    country_code: str
    code: str
    name: str
    count: int
    cost: float
    repeatable: bool
