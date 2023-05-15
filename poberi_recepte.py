import orodja
import re
import os
import csv

MAPA_OSNOVNIH_STRANI = "neobdelani-podatki/osnovne-strani"
MAPA_Z_RECEPTI = "neobdelani-podatki/recepti"
URL_OSNOVNA_STRAN = "https://www.skinnytaste.com/"
RECEPTI_CSV = "podatki_receptov.csv"


STEVILO_STRANI = 10
#STEVILO_RECEPTOV_NA_STRANI = 30


#--------------vzroci-------------------------------------------------------------------------------

# podatki, ki jih zajamemo:
# id_recepta
# oznake
# ime_recepta
# kategorije
# kulinarike
# cas_priprave
# cas_kuhanja
# st_porcij
# sestavine
# kalorije
# ogljikovi_hidrati
# mascobe
# beljakovine
# opis

VZOREC_RECEPTA = re.compile(
    r'"recipeYield":\["(?P<st_porcij>.*?)"[\n\s\S]*?'
    r'"articleSection":\[(?P<oznake>.*?)\][\n\s\S]*?'
    r'Calories"><span class="meta-label">Cals:</span> (?P<kalorije>.*?)</span> <span class="recipe-meta-value value-protein" title="Protein"><span class="meta-label">Protein:</span> (?P<beljakovine>.*?)</span> <span class="recipe-meta-value value-carbs" title="Carbohydrates"><span class="meta-label">Carbs:</span> (?P<ogljikovi_hidrati>.*?)</span> <span class="recipe-meta-value value-fat" title="Total Fat"><span class="meta-label">Fats:</span> (?P<mascobe>.*?)<[\n\s\S]*?'
    r'<h2 class="wprm-recipe-name wprm-block-text-normal">(?P<ime_recepta>.*?)</h2>[\n\s\S]*?'
    r'recipe-course-label">Course: </span><span class="wprm-recipe-course wprm-block-text-normal">(?P<kategorije>.*?)</span>[\n\s\S]*?'
    r'recipe-cuisine-label">Cuisine: </span><span class="wprm-recipe-cuisine wprm-block-text-normal">(?P<kulinarike>.*?)</span></div></div>[\n\s\S]*?'
    r'recipe-prep_time-.*?">(?P<cas_priprave>.*?)</span>.*?recipe-prep_timeunit-.*?">(?P<enota_priprave>.*?)</span>.*?recipe-cook_time-.*?">(?P<cas_kuhanja>.*?)</span>.*?recipe-cook_time-unit wprm-recipe-cook_timeunit-.*?">(?P<enota_kuhanja>.*?)<',
    flags=re.DOTALL
)
VZOREC_POSTOPKA = re.compile(
    r'type":"HowToStep","text":"(?P<korak>.*?)","name"',
    flags=re.DOTALL
)
VZOREC_SESTAVIN = re.compile(
    r'"wprm-recipe-ingredient-amount">(?P<kolicina_sestavine>.*?)</span>&#32;<span class="wprm-recipe-ingredient-unit">(?P<enota_sestavine>.*?)</span>&#32;<span class="wprm-recipe-ingredient-name">(?P<sestavina>.*?)<'
)

#---------------------------------------------------------------------------------------

# shrani osnovne strani ki so le "katalog" receptov

def poberi_osnovne_strani(ime_mape):
    for stran in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(ime_mape, f"stran_{stran}.html") 
        if stran == 1:
            url = URL_OSNOVNA_STRAN + f'recipe-index/'
        else:
            url = URL_OSNOVNA_STRAN + f'recipe-index/?_paged={stran}'
        print(url)
        orodja.shrani_spletno_stran(url, datoteka)


# iz vsake html datoteke osnovne strani pobere povezave na prave strani receptov
def najdi_povezave(vsebina):
    vzorec = r'<a href="https://www.skinnytaste.com/(.*?)/"><img width="260" height="390"'
    return re.findall(vzorec, vsebina)

def poberi_povezave_receptov_iz_osnovne_strani(mapa_s_stranmi):
    vse_povezave = []
    for i in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(mapa_s_stranmi, f"stran_{i}.html")
        osnovna_stran =  open(datoteka, "r",  encoding="utf-8")
        vsebina = osnovna_stran.read()
        povezave = najdi_povezave(vsebina)
        vse_povezave.extend(povezave)
        osnovna_stran.close()
    return vse_povezave

# ocisti tiste povezave, ki ne pripadaju pravemu receptu 
def dobre_povezave(povezave):
    pociscene_povezave = []
    st_dobrih = 0
    for povezava in povezave:
        if "7-day-healthy-meal" not in povezava and "popular-healthy-recipes" not in povezava and "mothers-day-gifts" not in povezava and "skinnytaste" not in povezava and "easy" not in povezava:
            pociscene_povezave.append(povezava)
            st_dobrih += 1
    return pociscene_povezave, st_dobrih

#odpre povezave receptov in jih prebere in shrani v html datoteke
def shrani_recepte(povezave, mapa_z_recepti):
    i = 1
    for povezava in povezave[0]:
        url = URL_OSNOVNA_STRAN + f"/{povezava}/"
        datoteka = os.path.join(mapa_z_recepti, f"recept_{i}.html")
        orodja.shrani_spletno_stran(url, datoteka)
        i += 1



#odpre html-je receptov in iz njih izlušči pomembne podatke
def podatki_receptov(mapa_z_recepti, st_receptov=213):
    seznam_podatkov = []
    for i in range(1, st_receptov + 1):
        datoteka = f"recept_{i}.html"
        pot = os.path.join(mapa_z_recepti, datoteka)
        if os.path.exists(pot):
            vsebina = orodja.vsebina_datoteke(pot)
            print(i)
            podatki_recepta = re.search(VZOREC_RECEPTA, vsebina)
            if podatki_recepta:
                recept = podatki_recepta.groupdict()
                recept["id_recepta"] = int(i)
                recept["oznake"] = recept["oznake"].strip().replace('"', '').split(",")
                recept["kategorije"] = recept["kategorije"].strip().split(",")
                recept["kulinarike"] = recept["kulinarike"].strip().split(",")
                recept["cas_priprave"] = int(recept["cas_priprave"]) 
                recept["cas_kuhanja"] = int(recept["cas_kuhanja"])
                recept["st_porcij"] = int(recept["st_porcij"])
                recept["kalorije"] = float(recept["kalorije"])
                recept["ogljikovi_hidrati"] = float(recept["ogljikovi_hidrati"])
                recept["mascobe"] = float(recept["mascobe"])
                recept["beljakovine"] = float(recept["beljakovine"])
                recept["sestavine"] = VZOREC_SESTAVIN.findall(vsebina)
                recept["postopek"] = VZOREC_POSTOPKA.findall(vsebina)
                seznam_podatkov.append(recept)
    return seznam_podatkov



#pomozna funkcija za locevanje podatkov
def seznam_slovarjev_podatkov(vrsta_podatka, id_recepta, seznam_podatkov):
    seznam_slovarjev = []
    for podatek in seznam_podatkov:
        seznam_slovarjev.append(
            {
                "id_recepta" : id_recepta,
                vrsta_podatka : podatek
            }
        )
    return seznam_slovarjev

def seznam_slovarjev_podatkov_sestavine(id_recepta, seznam_podatkov):
    seznam_slovarjev = []
    for podatek in seznam_podatkov:
        seznam_slovarjev.append(
            {
                "id_recepta" : id_recepta,
                "kolicina" : podatek[0],
                "enota" : podatek[1],
                "sestavina" : podatek[2]
            }
        )
    return seznam_slovarjev

def seznam_slovarjev_podatkov_postopek(id_recepta, seznam_podatkov):
    seznam_slovarjev = []
    for i in range(len(seznam_podatkov)):
        seznam_slovarjev.append(
            {
                "id_recepta" : id_recepta,
                "st_koraka" : i,
                "korak" : seznam_podatkov[i]
            }
        )
    return seznam_slovarjev

#s pomocjo prejsnjih funkcij izlusci podatke in zapise v csv
def poberi_in_zapisi_podatke():
    #poberi_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #vse_povezave = poberi_povezave_receptov_iz_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #povezave = dobre_povezave(vse_povezave)[0]
    #st_dobrih = dobre_povezave(vse_povezave)[1]
    #print(st_dobrih)
    #shrani_recepte(povezave, MAPA_Z_RECEPTI)
    recepti = podatki_receptov(MAPA_Z_RECEPTI)#, st_dobrih
    print("konec podatkov")

    vsi_recepti, vse_sestavine, vsi_postopki, vse_oznake, vse_kategorije, vse_kulinarike = [], [], [], [], [], []
    for recept in recepti:
        id_recepta = recept["id_recepta"]

        vsi_recepti.append(
            {
                "id_recepta" : recept["id_recepta"],
                "ime_recepta" : recept["ime_recepta"],
                "cas_priprave" : recept["cas_priprave"],
                "enota_priprave" : recept["enota_priprave"],
                "cas_kuhanja" : recept["cas_kuhanja"],
                "enota_kuhanja" : recept["enota_kuhanja"],
                "st_porcij" : recept["st_porcij"],
                "kalorije" : recept["kalorije"],
                "ogljikovi_hidrati" : recept["ogljikovi_hidrati"],
                "mascobe" : recept["mascobe"],
                "beljakovine" : recept["beljakovine"]
            }
        )
        vse_sestavine.extend(
            seznam_slovarjev_podatkov_sestavine(id_recepta, recept["sestavine"])
        )
        vsi_postopki.extend(
            seznam_slovarjev_podatkov_postopek(id_recepta, recept["postopek"])
        )
        vse_oznake.extend(
            seznam_slovarjev_podatkov("oznaka", id_recepta, recept["oznake"])
        )
        vse_kategorije.extend(
            seznam_slovarjev_podatkov("kategorija", id_recepta, recept["kategorije"])
        )
        vse_kulinarike.extend(
            seznam_slovarjev_podatkov("kulinarika", id_recepta, recept["kulinarike"])
        )

    #print(vse_oznake)
    #print(vse_kategorije)
    #print(vse_kulinarike)
    #print(vsi_recepti)

    orodja.zapisi_csv(
        vsi_recepti,
        ["id_recepta", "ime_recepta", "cas_priprave", "enota_priprave", "cas_kuhanja", "enota_kuhanja", "st_porcij", "kalorije",
            "ogljikovi_hidrati", "mascobe", "beljakovine"],
            "obdelani-podatki/recepti.csv"
    )
    orodja.zapisi_csv(vse_sestavine, ["id_recepta", "kolicina", "enota", "sestavina"], "obdelani-podatki/sestavine-receptov.csv")
    orodja.zapisi_csv(vsi_postopki, ["id_recepta", "st_koraka", "korak"], "obdelani-podatki/postopki.csv")
    orodja.zapisi_csv(vse_oznake, ["id_recepta", "oznaka"], "obdelani-podatki/oznake.csv")
    orodja.zapisi_csv(vse_kategorije, ["id_recepta", "kategorija"], "obdelani-podatki/kategorije.csv")
    orodja.zapisi_csv(vse_kulinarike, ["id_recepta", "kulinarika"], "obdelani-podatki/kulinarike.csv")
    print("konec csv")
    

poberi_in_zapisi_podatke()

#datoteka = 'recept_20.html'
#pot = os.path.join(MAPA_Z_RECEPTI, datoteka)
#vsebina = orodja.vsebina_datoteke(pot)
#podatki_recepta = re.search(VZOREC_RECEPTA, vsebina)
#recept = podatki_recepta.groupdict()
#recept["id_recepta"] = int(20)
#recept["oznake"] = recept["oznake"].strip().replace('"', '').split(",")
#recept["kategorije"] = recept["kategorije"].strip().split(",")
#recept["kulinarike"] = recept["kulinarike"].strip().split(",")
#recept["cas_priprave"] = int(recept["cas_priprave"]) 
#recept["cas_kuhanja"] = int(recept["cas_kuhanja"])
#recept["st_porcij"] = int(recept["st_porcij"])
#recept["kalorije"] = float(recept["kalorije"])
#recept["ogljikovi_hidrati"] = float(recept["ogljikovi_hidrati"])
#recept["mascobe"] = float(recept["mascobe"])
#recept["beljakovine"] = float(recept["beljakovine"])
#recept["sestavine"] = VZOREC_SESTAVIN.findall(vsebina)
#recept["postopek"] = VZOREC_POSTOPKA.findall(vsebina)
#
#
#seznam_podatkov = recept["postopek"]
#id_recepta = recept["id_recepta"]
#seznam_slovarjev = []
#for i in range(len(seznam_podatkov)):
#    seznam_slovarjev.append(
#        {
#            "id_recepta" : id_recepta,
#            "st_koraka" : i,
#            "korak" : seznam_podatkov[i]
#        }
#    )
#