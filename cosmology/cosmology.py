from __future__ import annotations
from typing import TYPE_CHECKING
from numpy import absolute, append
from numpy.random import default_rng, random_sample
from scipy.stats import skewnorm
from cosmology.element import Luminary

if TYPE_CHECKING:
    from numpy import ndarray

class Cosmology:
    """
    A Cosmology and its collection of important Elements.

    Parameters
    ----------
    seed : int, optional
        An integer used to seed the random number generation (RNG) used to
        populate the instance. If omitted, a random seed will be assigned.
    
    Attributes
    ----------
    luminary : list[Luminary]
        The Luminary instances important to this Cosmology.
    
    number : list[int]
        Numbers with some irreal significance to this Cosmology.
    
    """
    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            self.__seed = int(random_sample(size=1)[0] * (2**32 - 1))
        else:
            self.__seed = seed
        
        self.rng = default_rng(seed=self.__seed)
        
        self.luminary = self.__generate_luminaries()
        self.number = [len(list(filter(lambda l: l["visible"], self.luminary)))]
          
    def __repr__(self) -> str:
        return "{}(luminary={}, number={})".format(
            self.__class__.__name__,
            self.count("luminary"),
            self.number
        )
    
    def __generate_luminaries(self) -> list[Luminary]:
        """Randomized Luminary generation"""
        n = self.rng.integers(1, 13, 1)[0]

        dist = skewnorm.rvs(2, size=n, scale=15, random_state=self.rng)
        dist = absolute(append(dist, [0])).round(2)
        dist.sort()

        n += 1

        vis = dist <= 9.5
        rgb = self.rng.integers(0, 255, size=(n, 3), endpoint=True)

        return [Luminary(distance=dist[i], visible=vis[i], rgb=rgb[i])
                for i in range(n)]

    @property
    def seed(self) -> int:
        """Read-only access to the instance's `seed` attribute."""
        return self.__seed

    def count(self, element: str) -> int:
        """Return the count of Elements in this instance.

        Parameters
        ----------
        element: str
            The name of the desired Element.

        Returns
        -------
        int
            The number of Elements present in the instance.
        """
        return len(getattr(self, element.lower()))
