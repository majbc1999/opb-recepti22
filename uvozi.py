import pandas as pd
from pandas import DataFrame

from Data.Database import Repo
from Data.Modeli import *
from typing import Dict
from re import sub
import dataclasses

from model import Recepti


# Vse kar delamo z bazo se nahaja v razredu Repo.
repo = Repo()



def uvozi_recepte(pot):
    """
    Uvozimo csv z recepti v v bazo.
    Pri tem predpostavljamo, da imamo tabele že ustvarjene. 
    Vsako vrstico posebaj še obdelamo, da v bazi dobimo željeno strukturo. Uporabimo
    razred Repo za klic funkcij za uvoz v bazo.
    """

    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")

    # Iz stolpcev razberemo katera leta imamo
    recepti = dict()
    
    for row in df.itertuples():
        locena_vrstica = row.split(',')
        if locena_vrstica[3] != 'mins' or locena_vrstica[3] != 'hr':
            print(row)
        elif locena_vrstica[3] == 'hr':
            locena_vrstica[2] = 60 * int(locena_vrstica[2])
        else:
            continue

        if locena_vrstica[5] != 'mins' or locena_vrstica[5] != 'hr':
            print(row)
        elif locena_vrstica[5] == 'hr':
            locena_vrstica[4] = 60 * int(locena_vrstica[4])
        else:
            continue
        
        recept = repo.dodaj_recept(
            Recepti(
                ime=locena_vrstica[1],
                st_porcij=locena_vrstica[6],
                cas_priprave=locena_vrstica[2],
                cas_kuhanja=locena_vrstica[4] 
            )
        )

       

def uvozi_csv(pot, ime):
    """
    Uvozimo csv v bazo brez večjih posegov v podatke.
    Ustvarimo pandasov DataFrame ter nato z generično metodo ustvarimo ter
    napolnimo tabelo v postgresql bazi.
    """
    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")

    # Zamenjamo pomišljaje z prazno vrednostjo
    df.replace(to_replace="-", value="", inplace=True)

    # Naredimo tabelo z dodatnim serial primary key stolpcem
    repo.df_to_sql_create(df, ime, add_serial=True, use_camel_case=True)

    # uvozimo podatke v to isto tabelo
    repo.df_to_sql_insert(df, ime, use_camel_case=True)




# Primeri uporabe. Zakomentiraj določene vrstice, če jih ne želiš izvajat!
    

pot = "Data/cene.csv"



# Uvozi csv s cenami izdelkov v ločene (in povezane) entitete
# Tabele morajo biti prej ustvarjene, da zadeva deluje

# uvozi_cene(pot)

# Uvozi csv s cenami, le da tokar uvozi le eno tabelo, ki jo
# predhodno še ustvari, če ne obstaja.

# uvozi_csv(pot, "NovaTabela")




# S pomočjo generične metode dobimo seznam izdelkov in kategorij
# Privzete nastavi

# Dobimo prvih 100 izdelkov
izdelki = repo.dobi_gen(Izdelek, skip=0, take=100)

t = repo.dobi_gen(IzdelekDto)

# Dobimo prvih 10 kategorij
kategorije = repo.dobi_gen(KategorijaIzdelka)

# Dodamo novo kategorijo

nova_kategorija = KategorijaIzdelka(
    oznaka="Nova kategorija"
)

repo.dodaj_gen(nova_kategorija)

# vrednost nova_kategorija.id je sedaj določen na podlagi
# serial vrednosti iz baze in jo lahko uporabimo naprej.


# Dodamo nov izdelek v to kategorijo
novi_izdelek = Izdelek(
    ime = 'Novi izdelek',
    kategorija=nova_kategorija.id
)
repo.dodaj_gen(novi_izdelek)


# Dobimo izdelek z idjem 832
izdelek = repo.dobi_gen_id(Izdelek, 832)

# izdelku spremenimo ime in ga posodobimo v bazi
izdelek.ime += " spremenjeno ime"
repo.posodobi_gen(izdelek)



# spremenimo seznam izdelkov in ga shranimo v bazo

for i in izdelki:
    i.ime = f'({i.ime})'

repo.posodobi_list_gen(izdelki)
