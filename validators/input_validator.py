from typing import Any, Dict, List, Optional, Callable
import structlog
import spacy

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

nlp = spacy.load("en_core_web_sm")


@register_validator(name="input validator", data_type="string")
class InputValidator(Validator):
    def __init__(
        self,
        pos: List[str] = ["PNOUN", "NOUN"],
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail)
        self.pos = pos

    def _validate(self, value: str, metadata: Dict[str, Any] = {}) -> ValidationResult:
        try:
            line_index = metadata["index"]
            is_valid = False
            if len(value.split()) < 2:
                return self.error(
                    message=f"String too short in string ={value} at line {line_index}"
                )
            doc = nlp(value)
            for token in doc:
                if (
                    token.pos_ in self.pos
                ):  # Check for common noun (NOUN) or proper noun (PROPN)
                    is_valid = True
                    break
            return (
                PassResult()
                if is_valid
                else self.error(
                    message=f"Failed validation. No Nouns or PNouns detected in sentence: {value}."
                )
            )
        except Exception as e:
            return self.error(message=f"Unknon Exception occurred {e}")

    def error(self, message):
        return FailResult(
            error_message=message,
            fix_value="I'm sorry, I can't answer the question.",
        )


@register_validator(name="guardrails/two_words", data_type="string")
class TwoWords(Validator):
    """Validates that a value is two words.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `guardrails/two_words`            |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Pick the first two words.         |
    """

    def _get_fix_value(self, value: str) -> str:
        words = value.split()
        if len(words) == 1:
            # words = _words(value)
            pass

        if len(words) == 1:
            value = f"{value} {value}"
            words = value.split()

        return " ".join(words[:2])

    def validate(self, value: str, metadata: Dict) -> ValidationResult:
        """Validation method of this validator."""
        print("VALIDATE")
        # logger.debug(f"Validating {value} is two words...")

        if len(value.split()) != 2:
            return FailResult(
                error_message="Value must be exactly two words",
                fix_value=self._get_fix_value(value),
            )

        return PassResult()


# @register_validator(name="validate input", data_type="string")
# class InputValidator(Validator):
#     def __init__(self, on_fail=OnFailAction.Exception):
#         self.pos = []
#         super(on_fail)

#     def _validate(self, value: str, metadata: Dict[str, Any] = {}) -> ValidationResult:
#         try:
#             is_valid = False
#             doc = nlp(value)
#             line_index = metadata["index"]

#             if len(value) < 2:
#                 return self.error(
#                     message=f"String too short in string ={value} at line {line_index}"
#                 )

#             for token in doc:
#                 if (
#                     token.pos_ in self.pos
#                 ):  # Check for common noun (NOUN) or proper noun (PROPN)
#                     is_valid = True
#                     break

#             return (
#                 PassResult
#                 if is_valid
#                 else self.error(
#                     f"The string doesn't contain required POS, string={validated_text}"
#                 )
#             )
#         except Exception as e:
#             return self.error(message=f"Error {e}. String = {validated_text}")

#     def error(self, message):
#         return FailResult(
#             error_message=message,
#             fix_value="",
#         )
