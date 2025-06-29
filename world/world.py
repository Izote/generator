from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.noise import Noise, grid

if TYPE_CHECKING:
    from numpy import ndarray


class World:
    """A simulated World.

    Parameters
    ----------
    shape: tuple[int]
    
    """
    def __init__(self, shape: tuple[int, int]) -> None:
        self.__shape = shape
        self.map = self.__generate_noise()
    
    def __generate_noise(self) -> ndarray:
        generator = Noise(dimensions=2)
        
        return generator[grid(shape=self.__shape, scale=0.25, origin=(2, 0))]

    
    @property
    def shape(self) -> tuple[int, int]:
        """Read-only access to the instance's `shape` attribute."""
        return self.__shape
