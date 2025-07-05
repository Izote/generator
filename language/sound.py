from duckdb import connect
from utils import IPA_DB


class Sound:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.phonetic = symbol
        self.phonemic = symbol
        self.__quality = self._get_quality()
    
    def __repr__(self) -> str:
        quality = ", ".join([f"{k}='{v}'" if type(v) == str else f"{k}={v}"
                             for k, v in self.__quality.items()])
        
        return "{}(symbol='{}', phonetic='{}', phonemic='{}', {})".format(
            self.__class__.__name__,
            self.symbol,
            self.phonetic,
            self.phonemic,
            quality
        )

    def __str__(self) -> str:        
        if self.phonetic == self.phonemic:
            return f"'{self.symbol} [{self.phonetic}]'"
        else:
            return f"'{self.symbol} [{self.phonetic}] /{self.phonemic}/'"
    
    def _get_quality(self) -> dict:
        name = self.__class__.__name__.lower()

        if name == "consonant":
            key = ["voiced", "place", "manner"]
        else:
            key = ["height", "backness", "rounded"]
        
        column = ", ".join(key)

        query = f"SELECT {column} FROM {name} WHERE symbol = '{self.symbol}';"

        with connect(IPA_DB) as conn:
            value = conn.execute(query).fetchall()[0]
        
        return dict(zip(key, value))

class Consonant(Sound):
    def __init__(self, symbol: str) -> None:
        super().__init__(symbol=symbol)
    
    @property
    def voiced(self) -> bool:
        return self.__quality["voiced"]
    
    @property
    def place(self) -> str:
        return self.__quality["place"]
    
    @property
    def manner(self) -> str:
        return self.__quality["manner"]


class Vowel(Sound):
    def __init__(self, symbol: str) -> None:
        super().__init__(symbol=symbol)
    
    @property
    def height(self) -> str:
        return self.__quality["height"]
    
    @property
    def backness(self) -> str:
        return self.__quality["backness"]
    
    @property
    def rounded(self) -> bool:
        return self.__quality["rounded"]
