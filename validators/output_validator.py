import json
import random
from typing import Any, Dict, Optional, Callable
import pydantic
from pydantic import ValidationError

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="output validator", data_type="string")
class OutputValidatior(Validator):
    def __init__(
        self,
        pydantic_model: pydantic.BaseModel,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail)
        self.pydantic_model = pydantic_model

    def _validate(self, value: str, metadata: Dict[str, Any] = {}) -> ValidationResult:

        try:
            output_dict = json.loads(value)
            self.pydantic_model.model_validate(output_dict)
            return PassResult()
        except ValidationError as ve:
            return self.error(message=f"Pydantic Validation failed: {ve}")
        except Exception as e:
            return self.error(message=f"Validation failed: {e}")

    def error(self, message):
        return FailResult(
            error_message=message,
            fix_value="I'm sorry, I can't answer the question.",
        )
