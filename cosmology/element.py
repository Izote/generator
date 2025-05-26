class Element:
    """Any individual Element within a Cosmology.

    Attributes
    ----------
    **associations :
        Assign any irreal associations to the Element via keyword arguments.
        They may subsequently be accessed (re-assigned, updated, etc.) as keys
        from the Element itself (i.e., using `Element[key]`).

    """
    def __init__(self, **associations) -> None:
        self.__association = associations
    
    def __repr__(self) -> str:
        association = [f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" 
                       for k, v in self.__association.items()]
        
        return f"{self.__class__.__name__}({', '.join(association)})"
    
    def __getitem__(self, key: str) -> str | int | float | None:
        return self.__association[key]
    
    def __setitem__(self, key, value) -> None:
        self.__association[key] = value
