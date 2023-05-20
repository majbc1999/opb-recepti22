from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass

class Recepti:
    id: int = field(default=0)
    ime: str = field(default='')
    st_porcij: int = field(default=0)
    cas_priprave: int = field(default=0)
    cas_kuhanja: int = field(default=0) 
    id_uporabnika: int = field(default=0)

@dataclass

class ReceptPosSes:
    id_recepta: int = field(default=0)
    ime: str = field(default='')
    st_porcij: int = field(default=0)
    cas_priprave: int = field(default=0)
    cas_kuhanja: int = field(default=0) 
    postopek: str = field(default='')
    sestavine: str = field(default='')

@dataclass_json
@dataclass

class Postopki:
    id_recepta: int = field(default=0)
    st_koraka: int = field(default=0)
    postopek: str = field(default="")

@dataclass_json
@dataclass

class SestavineReceptov:
    id_recepta: int = field(default=0)
    kolicina: str = field(default='')
    enota: str = field(default='')
    sestavina: str = field(default='')

@dataclass_json
@dataclass

class Sestavine:
    id: int = field(default=0)
    ime: str = field(default="")
    kalorije : int = field(default=0)
    proteini : int = field(default=0)
    ogljikovi_hidrati : int = field(default=0)
    mascobe : int = field(default=0)

@dataclass

class NutrientskeVrednosti:
    id_recepta: int = field(default=0)
    kalorije : int = field(default=0)
    proteini : int = field(default=0)
    ogljikovi_hidrati : int = field(default=0)
    mascobe : int = field(default=0)

@dataclass_json
@dataclass

class Komentarji:
    id: int = field(default=0)
    avtor: str = field(default="")
    vsebina: str = field(default="")
    #datum

@dataclass_json
@dataclass

class Kategorije:
    id_recepta: int = field(default=0)
    kategorija: str = field(default="")

@dataclass_json

class VseKategorije:
    kategorija: str = field(default="")

@dataclass_json
@dataclass
class Kulinarike:
    id_recepta: int = field(default=0)
    kulinarika: str = field(default="")

@dataclass_json
@dataclass
class Oznake:
    id_recepta: int = field(default=0)
    oznaka: str = field(default="")

@dataclass_json
@dataclass
class Uporabnik:
    username: str = field(default="")
    id_uporabnika: int = field(default=0)
    password_hash: str = field(default="")
    last_login: str = field(default="")

@dataclass
class UporabnikDto:
    username: str = field(default="")
    id_uporabnika: int = field(default=0)