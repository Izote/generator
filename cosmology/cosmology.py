from __future__ import annotations
from typing import TYPE_CHECKING
from numpy import absolute, append, array
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
    
    number : ndarray[int]
        Numbers with some irreal significance to this Cosmology.
    
    """
    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            self.__seed = int(random_sample(size=1)[0] * (2**32 - 1))
        else:
            self.__seed = seed
        
        self.rng = default_rng(seed=self.__seed)
        
        self.luminary = self.__generate_luminaries()
        self.number = self.__generate_number()
          
    def __repr__(self) -> str:
        return "{}(luminary={}, number={})".format(
            self.__class__.__name__,
            self.count_attribute("luminary"),
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
    
    def __generate_number(self) -> ndarray:
        visible = len(list(filter(lambda l: l["visible"], self.luminary)))
        
        return array([visible])

    @property
    def seed(self) -> int:
        """Read-only access to the instance's `seed` attribute."""
        return self.__seed
    
    def add_number(self, n: int) -> None:
        """Add a new number to this instance.

        Parameters
        ----------
        n : int
            The desired number that will be added to this instance.
        
        Returns
        -------
        None

        """
        self.number = append(self.number, n)
    
    def remove_number(self, n: int) -> None:
        """Remove a number from this instance
        
        Parameters
        ----------
        n : int
            The desired number to remove from this instance.
        
        Returns
        -------
        None

        """
        self.number = self.number[self.number != n]

    def count_attribute(self, attribute: str) -> int:
        """Return the count of the desired attribute in this instance.

        Parameters
        ----------
        element: str
            The name of the desired attribute.

        Returns
        -------
        int
            The number of Elements present in the instance.
        """
        attr = getattr(self, attribute.lower())

        if isinstance(attr, list):
            return len(attr)
        else:
            return attr.shape[0]
