from __future__ import annotations

import json
from typing import Any


_REMOVED = object()


def exclude_non_public_elements(value: Any, *, exclude_none: bool) -> Any:
    filtered = _filter_non_public(value)
    if filtered is _REMOVED:
        return {}
    if exclude_none:
        return _prune_none_fields(filtered)
    return filtered


def dump_json(value: Any, *, indent: int | None, ensure_ascii: bool) -> str:
    if indent is None:
        return json.dumps(value, ensure_ascii=ensure_ascii, separators=(',', ':'))
    return json.dumps(value, ensure_ascii=ensure_ascii, indent=indent)


def _filter_non_public(value: Any) -> Any:
    if isinstance(value, list):
        items = []
        for item in value:
            filtered = _filter_non_public(item)
            if filtered is _REMOVED:
                continue
            items.append(filtered)
        return items

    if isinstance(value, dict):
        if 'access' in value and value['access'] != []:
            return _REMOVED

        items = {}
        for key, item in value.items():
            filtered = _filter_non_public(item)
            if filtered is _REMOVED:
                continue
            items[key] = filtered
        return items

    return value


def _prune_none_fields(value: Any) -> Any:
    if isinstance(value, list):
        return [_prune_none_fields(item) for item in value]

    if isinstance(value, dict):
        items = {}
        for key, item in value.items():
            if item is None:
                continue
            items[key] = _prune_none_fields(item)
        return items

    return value
