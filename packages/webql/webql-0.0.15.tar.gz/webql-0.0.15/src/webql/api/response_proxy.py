import json
from typing import Generic

from webql.common.aria_constants import CHECKBOX_ROLES, CLICKABLE_ROLES, INPUT_ROLES
from webql.common.errors import AttributeNotFoundError
from webql.web import InteractiveItemTypeT, WebDriver


class WQLResponseProxy(Generic[InteractiveItemTypeT]):
    def __init__(self, data: dict, web_driver: "WebDriver[InteractiveItemTypeT]"):
        self._response_data = data
        self._web_driver = web_driver

    def __getattr__(self, name) -> "WQLResponseProxy[InteractiveItemTypeT]" | InteractiveItemTypeT:
        if name not in self._response_data:
            raise AttributeNotFoundError(name, self._response_data)

        item = self._response_data[name]
        if _is_clickable(item) or _is_text_input(item) or _is_checkbox(item):
            return self._web_driver.locate_interactive_element(item)
        if isinstance(item, dict):
            return WQLResponseProxy[InteractiveItemTypeT](item, self._web_driver)

        return item

    def __str__(self):
        return json.dumps(self._response_data, indent=2)


def _is_clickable(node: dict) -> bool:
    return node.get("role") in CLICKABLE_ROLES


def _is_text_input(node: dict) -> bool:
    return node.get("role") in INPUT_ROLES


def _is_checkbox(node: dict) -> bool:
    return node.get("role") in CHECKBOX_ROLES
