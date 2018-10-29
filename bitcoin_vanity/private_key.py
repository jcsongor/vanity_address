from abc import ABC, abstractmethod
from secrets import randbits


class RNG(ABC):
    @abstractmethod
    def randbits(self, bits: int) -> int:
        pass


class SecretsRNG(ABC):
    def randbits(self, bits: int) -> int:
        return randbits(bits)


class PrivateKeyGenerator:
    _biggest_valid_private_key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140

    def __init__(self, rng: RNG):
        self._rng = rng

    def generate_private_key(self) -> int:
        while True:
            candidate = self._rng.randbits(256)
            if self._is_valid(candidate):
                return candidate

    def _is_valid(self, private_key_candidate: int) -> bool:
        return private_key_candidate <= self._biggest_valid_private_key
