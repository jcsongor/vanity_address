from abc import ABC, abstractmethod
from secrets import randbits


class RNG(ABC):
    @abstractmethod
    def randbits(self, bits: int) -> int:
        pass


class SecretsRNG(ABC):
    def randbits(self, bits: int) -> int:
        return randbits(bits)
