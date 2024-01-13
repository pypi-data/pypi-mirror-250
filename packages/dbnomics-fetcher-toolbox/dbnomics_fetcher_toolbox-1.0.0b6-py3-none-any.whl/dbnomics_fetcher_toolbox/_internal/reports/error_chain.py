from typing import NotRequired, TypedDict

__all__ = ["build_error_chain"]


class ErrorChainNode(TypedDict):
    cause: NotRequired["ErrorChainNode"]
    message: str
    type: str


def build_error_chain(error: BaseException) -> ErrorChainNode:
    if error is None:
        return None
    message = str(error)
    node: ErrorChainNode = {"message": message, "type": type(error).__qualname__}
    if error.__cause__ is not None:
        node["cause"] = build_error_chain(error.__cause__)
    return node
