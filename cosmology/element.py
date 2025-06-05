from __future__ import annotations
from typing import TYPE_CHECKING
from re import match
from numpy import array, where
from numpy.linalg import norm

if TYPE_CHECKING:
    from numpy import ndarray


class Element:
    """
    Any individual Element within a Cosmology.

    Parameters
    ----------
    **associations :
        Assign any irreal associations to the Element via keyword arguments.
        They may subsequently be accessed (re-assigned, updated, etc.) as keys
        from the Element itself (i.e., using `Element[key]`).

    """
    def __init__(self, **associations) -> None:
        for k, v in associations.items():
            setattr(self, k, v)
    
    def __repr__(self) -> str:
        def not_dunder(x):
            return match("^_", x) is None
        
        attribute = dir(self)
        if "name" in attribute:
            other = filter(lambda x: x != "name" and not_dunder(x), attribute)
            key = ["name"] + list(other)
        else:
            key = [k for k in attribute if not_dunder(k)]
        
        value = [getattr(self, k) for k in key]
        index = [i for i in range(len(value)) if not callable(value[i])]

        text = []
        for i in index:
            template = "{}='{}'" if isinstance(value[i], str) else "{}={}"
            text.append(template.format(key[i], value[i]))
        
        return f"{self.__class__.__name__}({', '.join(text)})"
    
    def __getitem__(self, key: str) -> str | int | float | None:
        return getattr(self, key)
    
    def __setitem__(self, key, value) -> None:
        setattr(self, key, value)


class Luminary(Element):
    """
    Any Luminary (e.g., sun, moon, star, planet, etc.) within a Cosmology.

    Parameters
    ----------
    distance : float
        How far the Luminary is from the Sun in Astronomical units (AU). The
        Sun itself will be at `distance=0.0`.

    visible : bool
        Whether the Luminary is visible to the naked eye.

    rgb : ndarray
        A 3-element array describing the Luminary's visible color as RGB values.
    
    Attributes
    ----------
    distance : float
        This Luminary's distance from its Sun in astronomical units (AU).
    
    visible : bool
        Whether this Luminary is visible with the naked eye.
    
    rgb : ndarray
        The RGB color value this Luminary appears as in the night sky.
    
    color : str
        A text description of the Luminary's RGB color.
    
    """
    def __init__(self, distance: float, visible: bool, rgb: ndarray) -> None:
        super().__init__(
            distance=distance,
            visible=visible,
            rgb=rgb,
            color=self.__describe_rgb(rgb)
            )
    
    def __describe_rgb(self, rgb: ndarray) -> str:
        """Describe a rgb value array as a string."""
        name = ["orange", "red", "green", "blue", "white"]
        value = array([[255, 165, 0],[255, 0, 0],[0, 255, 0],[0, 0, 255],
                       [255, 255, 255]])

        distance = norm(value - rgb, axis=1)
        closest = where(distance == distance.min())[0][0]
        
        return name[closest]
