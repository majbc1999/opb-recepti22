from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass

class Recept:
    id: int = field(default=0)
    ime: str = field(default='')
    st_porcij: int = field(default=0)
    cas_priprave: int = field(default=0)
    cas_kuhanja: int = field(default=0) 

@dataclass

class Postopek:
    postopek: str = field(default="")

@dataclass_json
@dataclass

class Sestavine:
    id: int = field(default=0)
    ime: str = field(default="")
    mascobe : int = field(default=0)
    ogljikovi_hidrati : int = field(default=0)
    kalorije : int = field(default=0)
    proteini : int = field(default=0)

@dataclass

class NutrienstkaVrednost:
    id: int = field(default=0)
    mascobe : int = field(default=0)
    ogljikovi_hidrati : int = field(default=0)
    kalorije : int = field(default=0)
    proteini : int = field(default=0)

@dataclass_json
@dataclass

class Uporabnik:
    id: int = field(default=0)
    ime: str = field(default="")

@dataclass_json
@dataclass

class Komentarji:
    id: int = field(default=0)
    avtor: str = field(default="")
    vsebina: str = field(default="")
    #datum

@dataclass_json
@dataclass

class TipiReceptov:
    id: int = field(default=0)
    ime: str = field(default="")
