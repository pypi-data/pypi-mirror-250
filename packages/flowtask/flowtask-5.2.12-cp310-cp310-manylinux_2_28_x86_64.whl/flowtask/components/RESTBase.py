"""RESTBase.

Basic component for making RESTful queries to URLs.
"""
import asyncio
from abc import ABC
from typing import (
    List,
    Dict,
    Union
)
from collections.abc import Callable
from urllib.parse import urlencode
from flowtask.exceptions import (
    DataNotFound,
    ComponentError
)
from .HTTPClient import HTTPClient


class RESTBase(HTTPClient, ABC):
    """
    RESTBase.

    Overview

         This Component Inherits the HTTPClient method

    .. table:: Properties
       :widths: auto

    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self._result: Union[List, Dict] = None
        self.accept: str = 'application/json'  # by default
        self._method: str = kwargs.pop('method', None)
        super(RESTBase, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if not hasattr(self, self._method):
            raise ComponentError(
                f'{self.__name__} Error: has no Method {self._method}'
            )
        # Getting the method to be called
        self._fn = getattr(self, self._method)
        await super(RESTBase, self).start(
            **kwargs
        )

    async def run(self):
        return self._result
