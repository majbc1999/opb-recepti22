import re
import orodja
import os
from string import ascii_uppercase


##############################################################################
# Poberem vse spletne strani

def shrani_po_abecedi():
    seznam_crk_brez_A = [''] + list(ascii_uppercase)[1:]
    for crka in seznam_crk_brez_A:
        ime_datoteke = crka + '.html'
        url = 'http://www.nutritiontable.com/nutritions/{}/'.format(crka)
        orodja.shrani_spletno_stran(url, ime_datoteke)

def datoteke_po_abecedi():
    seznam = []
    seznam_crk = list(ascii_uppercase)
    for crka in seznam_crk:
        seznam += [crka + '.html']
    return seznam
    
###############################################################################    

# Vzorci, ki jih bomo potrebovali za zajem podatkov

vzorec_bloka = re.compile(
    r'<div id="cphMain_ltvNutrition_pnlRowContainer[\n\s\S]*?'
    r'<span id="cphMain_ltvNutrition_lblHealty',
    flags = re.DOTALL
)

vzorec_sestavine = re.compile(
    r'<span id="cphMain_ltvNutrition_lblprodName.*?'
    r'href="/nutritions/nutrient.*?">(?P<ime>.*?)</a>',  
    flags=re.DOTALL
)

vzorec_cal = re.compile(r'<span id="cphMain_ltvNutrition_lblKcal_\d*?">(?P<kalorije>.*?)</span>', flags=re.DOTALL)
vzorec_kjoule = re.compile(r'<span id="cphMain_ltvNutrition_lblKjoule_\d*?">(?P<kjoule>.*?)</span>', flags=re.DOTALL)
vzorec_voda = re.compile(r'<span id="cphMain_ltvNutrition_lblWater_\d*?">(?P<voda>.*?)</span>', flags=re.DOTALL)
vzorec_proteini = re.compile(r'<span id="cphMain_ltvNutrition_lblEiwit_\d*?">(?P<proteini>.*?)</span>', flags=re.DOTALL)
vzorec_oh = re.compile(r'<span id="cphMain_ltvNutrition_lblKoolh_\d*?">(?P<ogljikovi_hidrati>.*?)</span>', flags=re.DOTALL)
vzorec_sladkor = re.compile(r'<span id="cphMain_ltvNutrition_lblKoolh_\d*?">(?P<sladkor>.*?)</span>', flags=re.DOTALL)
vzorec_mascobe = re.compile(r'<span id="cphMain_ltvNutrition_lblVet_\d*?">(?P<mascobe>.*?)</span>', flags=re.DOTALL)
vzorec_vlaknine = re.compile(r'<span id="cphMain_ltvNutrition_lblVoedv_\d*?">(?P<vlaknine>.*?)</span>', flags=re.DOTALL)


# Za vsako sestavino izločimo podatke o njej
def izloci_podatke_sestavine(blok):
    sestavina = vzorec_sestavine.search(blok).groupdict()
    
    sestavina['ime'] = sestavina['ime'].replace(',', '')

    cal = vzorec_cal.search(blok)
    if cal and cal != '':
        sestavina['kalorije'] = int(cal['kalorije'])
    else:
        sestavina['kalorije'] = None

    kjoule = vzorec_kjoule.search(blok)
    if kjoule and kjoule != '':
        sestavina['kjoule'] = int(kjoule['kjoule'])
    else:
        sestavina['kjoule'] = None
        
    voda = vzorec_voda.search(blok)
    if voda and voda != '':
        sestavina['voda'] = voda['voda'].replace(',','.')
    else:
        sestavina['voda'] = None
    
    pro = vzorec_proteini.search(blok)
    if pro and pro != '':
        sestavina['proteini'] = pro['proteini'].replace(',','.')
    else:
        sestavina['proteini'] = None
    
    oh = vzorec_oh.search(blok)
    if oh and oh != '':
        sestavina['ogljikovi hidrati'] = oh['ogljikovi_hidrati'].replace(',','.')
    else:
        sestavina['ogljikovi hidrati'] = None
    
    sladkor = vzorec_sladkor.search(blok)
    if sladkor and sladkor != '':
        sestavina['sladkor'] = sladkor['sladkor'].replace(',','.')
    else:
        sestavina['sladkor'] = None
    
    mascobe = vzorec_mascobe.search(blok)
    if mascobe and mascobe != '':
        sestavina['mascobe'] = mascobe['mascobe'].replace(',','.')
    else:
        sestavina['mascobe'] = None

    vlaknine = vzorec_vlaknine.search(blok)
    if vlaknine and vlaknine != '':
        sestavina['vlaknine'] = vlaknine['vlaknine'].replace(',','.')
    else:
        sestavina['vlaknine'] = None

    return sestavina

# Poiščemo bloke za vsako od sestavin 
def sestavine_v_datoteki(datoteka):
    vsebina = orodja.vsebina_datoteke(datoteka)
    for blok in re.findall(vzorec_bloka, vsebina):
        yield izloci_podatke_sestavine(blok)


sestavine = []
for datoteka in datoteke_po_abecedi():
    for sestavina in sestavine_v_datoteki(datoteka):
        sestavine.append(sestavina)
sestavine.sort(key=lambda sestavine: sestavine['ime'])

orodja.zapisi_csv(
    sestavine,
    ['ime', 
    'kalorije', 
    'kjoule', 
    'voda', 
    'proteini', 
    'ogljikovi hidrati', 
    'sladkor', 
    'mascobe', 
    'vlaknine'],
    'obdelani-podatki/sestavine.csv')