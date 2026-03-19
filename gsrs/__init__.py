from . import model

__all__ = ["model"]


def __getattr__(name: str):
    return getattr(model, name)
