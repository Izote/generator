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
    seed : int
        The integer seed used for this instance and its members.

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
        """Generate a list of Luminary objects."""
        n, scale = self.rng.integers(4, 16, 2)

        # Appending a {0, 1} values to stand-in for Sol, Earth respectively.
        dist = skewnorm.rvs(2, size=n, scale=scale, random_state=self.rng)
        dist = append(dist, [0.00])
        
        if 1.00 not in dist:
            dist = append(dist, [1.00])
        
        dist = absolute(dist).round(2)
        dist.sort()

        n += 1

        vis = dist <= 9.5

        # Forcing 0th element to be orange, keeping with theme.
        rgb = self.rng.integers(0, 255, size=(n, 3), endpoint=True)
        rgb[0] = array([255, 165, 0])

        return [Luminary(distance=dist[i], visible=vis[i], rgb=rgb[i])
                for i in range(n)]
    
    def __generate_number(self) -> ndarray:
        """Generate an initial array of important numbers."""
        visible = len(list(filter(lambda l: l["visible"], self.luminary)))
        
        return array([visible])

    @property
    def seed(self) -> int:
        """Read-only access to the instance's `seed` attribute."""
        return self.__seed
    
    def add_number(self, n: int) -> None:
        """Add a significant number to this instance.

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
        """Remove a significant number from this instance.
        
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
        """Count of the items within the desired attribute.

        Parameters
        ----------
        element: str
            The name of the desired attribute.

        Returns
        -------
        int
            The number of items present in the selected attribute.
        """
        attr = getattr(self, attribute.lower())

        if isinstance(attr, list):
            return len(attr)
        else:
            return attr.shape[0]
