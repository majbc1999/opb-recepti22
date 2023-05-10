import pandas as pd
from pandas import DataFrame

from Database import Repo
from model import *
from typing import Dict
from re import sub
import dataclasses



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
        
        repo.dodaj_recept(
            Recept(
                ime=locena_vrstica[1],
                st_porcij=locena_vrstica[6],
                cas_priprave=locena_vrstica[2],
                cas_kuhanja=locena_vrstica[4] 
            )
        )

def uvozi_kategorije(pot):
    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")


    for row in df.itertuples():
        locena_vrstica = row.split(',')

        repo.dodaj_kategorijo(

            Kategorija(
            ime = locena_vrstica[1],
            )
        )

def uvozi_sestavine_receptov(pot):
    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")


    for row in df.itertuples():
        locena_vrstica = row.split(',')

        repo.dodaj_sestavino(

            SestavineReceptov(
            id = locena_vrstica[0],
            ime = locena_vrstica[1],
            )
        )


def uvozi_postopke(pot):
    df = pd.read_csv(pot, sep=";",skiprows=[0], encoding="Windows-1250")

    #ne smemo lociti na vejice, saj se pojavijo tudi v povedih!
    for row in df.itertuples():
        locena_vrstica = row.split(',', 2)

        repo.dodaj_postopek(

            Postopek(
            id = locena_vrstica[0],
            st_koraka = locena_vrstica[1],
            postopek = locena_vrstica[2],
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
    

pot = "obelani_podatki/recepti.csv"
##pot = "obelani_podatki/kategorije.csv"
##pot = "obelani_podatki/sestavine_receptov.csv"
##pot = "obelani_podatki/postopki.csv"

# Uvozi csv s cenami izdelkov v ločene (in povezane) entitete
# Tabele morajo biti prej ustvarjene, da zadeva deluje

uvozi_recepte(pot)
##uvozi_kategorije(pot)
##uvozi_sestavine_receptov(pot)
##uvozi_postopke(pot)

# Uvozi csv s cenami, le da tokar uvozi le eno tabelo, ki jo
# predhodno še ustvari, če ne obstaja.

uvozi_csv(pot, "NovaTabela")



## A TO SPLOH RABVA? NE RAZUMM CIST KAJ DELA SPODNJA STVAR? USTVARJA NOVE KATEGORIJE?
# S pomočjo generične metode dobimo seznam izdelkov in kategorij
# Privzete nastavi

# Dobimo prvih 100 izdelkov
recepti = repo.dobi_gen(Recept, skip=0, take=100)

t = repo.dobi_gen(ReceptPosSes)

# Dobimo prvih 10 kategorij
kategorije = repo.dobi_gen(Kategorija)

# Dodamo novo kategorijo

nova_kategorija = Kategorija(
    oznaka="Nova kategorija"
)

repo.dodaj_gen(nova_kategorija)

# vrednost nova_kategorija.id je sedaj določen na podlagi
# serial vrednosti iz baze in jo lahko uporabimo naprej.


# Dodamo nov recept v to kategorijo
novi_recept = Recept(
    ime = 'Novi recept',
    kategorija=nova_kategorija.id
)
repo.dodaj_gen(novi_recept)


# Dobimo recept z idjem 832
recept = repo.dobi_gen_id(Recept, 832)

# izdelku spremenimo ime in ga posodobimo v bazi
recept.ime += " spremenjeno ime"
repo.posodobi_gen(recept)



# spremenimo seznam receptov in ga shranimo v bazo

for i in recepti:
    i.ime = f'({i.ime})'

repo.posodobi_list_gen(recepti)
