from typing import NoReturn

from cyrenebot.infra.adapters.openai_compatible.errors import translate_openai_error


def raise_openai_error(exc: Exception) -> NoReturn:
    raise translate_openai_error(exc) from exc
