from typing import Any, Dict, Optional, Union

from aiohttp import ClientResponse


def _shorten_error_dict(d, parent_key: str = "") -> dict[str, str]:
    ret_items: dict[str, str] = {}

    _errors = d.get("_errors")
    if _errors is not None and isinstance(_errors, list):
        ret_items[parent_key] = ", ".join([msg["message"] for msg in _errors])
    else:
        for key, value in d.items():
            key_path = f"{parent_key}.{key}" if parent_key else key
            # pyright thinks the type of value could be object which violates the first parameter
            # of this function
            ret_items |= list(_shorten_error_dict(value, key_path).items())  # type: ignore

    return ret_items


class BaseException(Exception):
    pass


class HTTPException(BaseException):
    def __init__(self, response: ClientResponse, message: Optional[Union[str, Dict[str, Any]]]):
        self.response = response
        self.status: int = response.status
        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get("code", 0)
            base = message.get("message", "")
            errors = message.get("errors")
            self._errors: Optional[Dict[str, Any]] = errors
            if errors:
                errors = _shorten_error_dict(errors)
                helpful = "\n".join("In %s: %s" % t for t in errors.items())
                self.text = base + "\n" + helpful
            else:
                self.text = base
        else:
            self.text = message or ""
            self.code = 0

        fmt = "{0.status} {0.reason} (error code: {1})"
        if len(self.text):
            fmt += ": {2}"

        super().__init__(fmt.format(self.response, self.code, self.text))
