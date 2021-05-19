from typing import List


class ValidationError(Exception):
    def __init__(self, field_name: str, errors: List[str], *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.field_name = field_name
        self.errors = errors
