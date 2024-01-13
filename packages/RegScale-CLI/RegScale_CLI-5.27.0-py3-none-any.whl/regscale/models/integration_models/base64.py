"""Standard imports"""
import base64


class Base64String(str):
    """Base64 String"""

    @classmethod
    def __get_validators__(cls):
        """Get validators"""
        yield cls.validate

    @classmethod
    def validate(cls, input_string: str):
        """Validate base64 string"""
        try:
            base64.b64decode(input_string)
            return input_string
        except Exception as exc:
            raise ValueError from exc
