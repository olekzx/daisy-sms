from dataclasses import dataclass
from .activation_status import ActivationStatus


@dataclass(frozen=True)
class GetCodeResponse:
    status: ActivationStatus
    code: int | None = None
