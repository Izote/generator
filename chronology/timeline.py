from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from itertools import count
from .event import Event

if TYPE_CHECKING:
    from typing import Callable


class Timeline:
    """Represents a series of days and related sequences of Events.
    
    Parameters
    ----------
    None

    Attributes
    ----------

    event : list
        A list of Events where each index maps directly to a sequential day 
        (i.e., day 0 = index 0). Multiple Events on a single day will be stored
        as a nested list. An index without any recorded Events will be None.

    """
    __default_format = lambda x: f"{x} days have elapsed."

    def __init__(self) -> None:
        self.__count = count()
        self.__format = __class__.__default_format
        self.__value = next(self.__count)
        self.event = [None]
        
    
    def __setitem__(self, key: int, item: Event | list[Event]) -> None:
        item_type = type(item)
        
        if item_type in {Event, list}:
            self.event[key] = item if item_type == list else [item]
        else:
            error = f"`{item_type}` items cannot be added to the Timeline."
            
            raise TypeError(error)


    def __getitem__(self, key: int) -> list[Event] | None:
        return self.event[key]

    @property
    def date(self) -> str:
        """Return date as stylized `str`."""
        return self.__format(self.__value)
    
    @property
    def day(self) -> int:
        """Return current day as int."""
        return self.__value

    def progress(self, days: int = 1) -> None:
        """Move the Timeline forward by a number of days.
        
        Parameters
        ----------
        days : int
            A number of days to add to the Timeline. Defaults to 1.
        
        Returns
        -------
        None

        """
        for _ in range(days):
            self.__value = next(self.__count)
            self.event.append(None)

    def set_format(self, format_method: Callable | None) -> None:
        """Set a new method for subsequent date formatting.

        Parameters
        ----------
        format_method : callable
            A function that converts a single int (i.e., the Timeline's value)
            to a stylized date format (i.e., `str` output). Passing None will
            reset to the default format style.

        Returns
        -------
        None

        """
        if format_method is None:
            self.__format = __class__.__default_format
        else:
            self.__format = format_method
