from dataclasses import dataclass


@dataclass(frozen=True)
class RentNumberResponse:
    id: int
    number: int
