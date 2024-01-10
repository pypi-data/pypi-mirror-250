from abc import abstractmethod
from typing import Optional
from urllib import parse

import requests
from aiohttp import ClientSession, ClientTimeout

from tablegpt_executor_client.errors import parse_error
from tablegpt_executor_client.schemas import (
    BatchOperation,
    ExecutionResult,
    SingleOperation,
)


class Client:
    """Tablegpt Executor Client"""

    @abstractmethod
    def execution(self, single_operation: SingleOperation) -> ExecutionResult:
        ...

    @abstractmethod
    def batch_execution(self, batch_operation: BatchOperation) -> ExecutionResult:
        ...


class SyncClient(Client):
    """Sync Client"""

    def __init__(
        self,
        base_url: str,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[dict[str, str]] = None,
        timeout: int = 10,
    ):
        self.base_url = base_url
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout

    def execution(
        self,
        single_operation: SingleOperation,
    ) -> ExecutionResult:
        payload = self._send_request(
            path="/execution", data=single_operation.model_dump()
        )
        return ExecutionResult.model_validate(payload)

    def batch_execution(
        self,
        batch_operation: BatchOperation,
    ) -> ExecutionResult:
        payload = self._send_request(
            path="/batch-execution", data=batch_operation.model_dump()
        )
        return ExecutionResult.model_validate(payload)

    def _send_request(self, path: str, data: dict):
        resp = requests.post(
            url=parse.urljoin(self.base_url, path),
            json=data,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
        )
        payload = resp.json()
        if resp.status_code not in (200, 201):
            raise parse_error(resp.status_code, payload)
        return payload


class AsyncClient(Client):
    """Async Client"""

    def __init__(
        self,
        base_url: str,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[dict[str, str]] = None,
        timeout: int = 10,
    ):
        self.base_url = base_url
        self.headers = headers
        self.cookies = cookies
        self.timeout = ClientTimeout(timeout * 60)

    async def execution(
        self,
        single_operation: SingleOperation,
        message_queue_key: Optional[str] = None,
    ) -> ExecutionResult:
        async with ClientSession(
            headers=self.headers, cookies=self.cookies, timeout=self.timeout
        ) as session:
            async with session.post(
                parse.urljoin(self.base_url, "/execution"),
                params={"message_queue_key": message_queue_key},
                json=single_operation.model_dump(),
            ) as resp:
                payload = await resp.json()

                if resp.status not in (200, 201):
                    raise parse_error(resp.status, payload)
                return ExecutionResult.model_validate(payload)

    async def batch_execution(
        self,
        batch_operation: BatchOperation,
    ) -> ExecutionResult:
        async with ClientSession(
            headers=self.headers, cookies=self.cookies, timeout=self.timeout
        ) as session:
            async with session.post(
                parse.urljoin(self.base_url, "/batch-execution"),
                json=batch_operation.model_dump(),
            ) as resp:
                payload = await resp.json()

                if resp.status not in (200, 201):
                    raise parse_error(resp.status, payload)
                return ExecutionResult.model_validate(payload)
