from re import match


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
        for k, v in associations.items():
            setattr(self, k, v)
    
    def __repr__(self) -> str:
        def not_dunder(x):
            return match("^_", x) is None
        
        def is_data_type(x):
            return any([
                isinstance(x, str),
                isinstance(x, int),
                isinstance(x, float),
                isinstance(x, bool)
                ])
        
        attribute = dir(self)
        if "name" in attribute:
            other = filter(lambda x: x != "name" and not_dunder(x), attribute)
            key = ["name"] + list(other)
        else:
            key = [k for k in attribute if not_dunder(k)]
        
        value = [getattr(self, k) for k in key]
        index = [i for i in range(len(value)) if is_data_type(value[i])]

        text = []
        for i in index:
            template = "{}='{}'" if isinstance(value[i], str) else "{}={}"
            text.append(template.format(key[i], value[i]))
        
        return f"{self.__class__.__name__}({', '.join(text)})"
    
    def __getitem__(self, key: str) -> str | int | float | None:
        return getattr(self, key)
    
    def __setitem__(self, key, value) -> None:
        setattr(self, key, value)
