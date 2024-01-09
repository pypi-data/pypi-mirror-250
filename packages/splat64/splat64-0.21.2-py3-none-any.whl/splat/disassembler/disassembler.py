from abc import ABC, abstractmethod
from typing import Set


class Disassembler(ABC):
    @abstractmethod
    def configure(self):
        raise NotImplementedError("configure")

    @abstractmethod
    def check_version(self, skip_version_check: bool, splat_version: str):
        raise NotImplementedError("check_version")

    @abstractmethod
    def known_types(self) -> Set[str]:
        raise NotImplementedError("known_types")
