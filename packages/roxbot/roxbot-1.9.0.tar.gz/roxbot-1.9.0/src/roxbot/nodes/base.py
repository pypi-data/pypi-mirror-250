#!/usr/bin/env python3
"""
 Base classes for node system

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

from abc import ABC, abstractmethod
import logging


class Node(ABC):
    """system node class"""

    def __init__(self, name: str) -> None:
        self.name = name

        # logger
        self.log = logging.getLogger(name)

    @abstractmethod
    async def main(self):
        """main coroutine"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"
