from __future__ import annotations

import httpx

from cyrenebot.core.errors.tool import ToolExecutionError
from cyrenebot.core.schema.tool import ToolCall, ToolResult
from cyrenebot.infra.adapters.tools.common import (
    make_tool_payload,
    map_json_text_tool_result,
    map_tool_result,
    map_tool_result_object,
    parse_tool_arguments,
)


class HttpToolExecutor:
    """
    HTTP 工具执行器
    """

    def __init__(
        self,
        url: str,
        *,
        method: str = "POST",
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._url = url
        self._method = method
        self._headers = headers or {}
        self._timeout = timeout
        self._client = client

    async def execute(self, call: ToolCall) -> ToolResult:
        """
        执行 HTTP 工具
        """
        arguments = parse_tool_arguments(call.arguments)
        payload = make_tool_payload(call, arguments)

        try:
            response = await self._request(payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ToolExecutionError(
                f"Tool {call.name} HTTP request failed with "
                f"status {exc.response.status_code}",
                cause=exc,
            ) from exc
        except httpx.HTTPError as exc:
            raise ToolExecutionError(
                f"Tool {call.name} HTTP request failed",
                cause=exc,
            ) from exc

        return map_http_response(call, response)

    async def _request(self, payload: dict) -> httpx.Response:
        if self._client is not None:
            return await self._client.request(
                self._method,
                self._url,
                json=payload,
                headers=self._headers,
            )

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            return await client.request(
                self._method,
                self._url,
                json=payload,
                headers=self._headers,
            )


def map_http_response(call: ToolCall, response: httpx.Response) -> ToolResult:
    """
    将 HTTP 响应映射为 ToolResult
    """
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        return map_json_text_tool_result(call, response.text)

    payload = response.json()
    if isinstance(payload, dict):
        return map_tool_result_object(call, payload)
    return map_tool_result(call, response.text)
