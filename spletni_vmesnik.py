from operator import mod
import bottle 
import bottletext
import model
import Database

r = Database.Repo()
kategorije = [x.kategorija for x in r.dobi_razlicne_gen(model.Kategorije, 'kategorija', 181, 0)]
kulinarike = [x.kulinarika for x in r.dobi_razlicne_gen(model.Kulinarike, 'kulinarika', 181, 0)]
oznake = [x.oznaka for x in r.dobi_razlicne_gen(model.Oznake, 'oznaka', 181, 0)]
vse_sestavine = r.dobi_vse_gen(model.Sestavine)

@bottle.get('/')
def vsi_recepti():
    recepti = r.dobi_vse_gen(model.Recepti)
    return bottle.template('views/front-page.tpl', kategorije=kategorije,
                                                    kulinarike=kulinarike,
                                                    oznake=oznake,
                                                    recepti=recepti)


@bottle.get('/recepti-kategorije/<kategorija>')
def doloceni_recepti(kategorija):
    seznam_idjev = r.dobi_gen_ime(model.Kategorije, kategorija, 'kategorija')
    recepti_izbrane_kategorije = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return bottle.template('views/doloceni_recepti_kategorije.tpl', kategorija=kategorija,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kategorije)

@bottle.get('/recepti-kulinarike/<kulinarika>')
def doloceni_recepti(kulinarika):
    seznam_idjev = r.dobi_gen_ime(model.Kulinarike, kulinarika, 'kulinarika')
    recepti_izbrane_kulinarike = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return bottle.template('views/doloceni_recepti_kulinarike.tpl', kulinarika=kulinarika,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kulinarike)

@bottle.get('/recepti-oznake/<oznaka>')
def doloceni_recepti(oznaka):
    seznam_idjev = r.dobi_gen_ime(model.Oznake, oznaka, 'oznaka')
    recepti_izbrane_oznake = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return bottle.template('views/doloceni_recepti_oznake.tpl', oznaka=oznaka,
                                                                kategorije=kategorije,
                                                                kulinarike=kulinarike,
                                                                oznake=oznake,
                                                                recepti=recepti_izbrane_oznake)

@bottle.post('/<id>/')
def pojdi_na_recept(id):
    return bottle.redirect('/recept/{}'.format(id))

@bottle.get('/recept/<id>')
def recept(id):
    recept = r.dobi_gen_id(model.Recepti, id,'id')
    sestavine = r.dobi_vse_gen_id(model.SestavineReceptov, id,'id_recepta')
    postopek = r.dobi_vse_gen_id(model.Postopki, id,'id_recepta')
    nutrientske_vrednosti = r.dobi_nutrientske_vrednosti(id)
    kategorije_recepta = r.dobi_vse_gen_id(model.Kategorije, id,'id_recepta')
    kulinarike_recepta = r.dobi_vse_gen_id(model.Kulinarike, id,'id_recepta')
    oznake_recepta = r.dobi_vse_gen_id(model.Oznake, id,'id_recepta')

    return bottle.template('views/recept.tpl', id=id,
                                               kategorije=kategorije,
                                               kulinarike=kulinarike,
                                               oznake=oznake,
                                               recept=recept,
                                               sestavine_recepta=sestavine,
                                               postopek=postopek,
                                               nutrientske_vrednosti=nutrientske_vrednosti,
                                               kategorije_recepta=kategorije_recepta,
                                               kulinarike_recepta=kulinarike_recepta,
                                               oznake_recepta=oznake_recepta,
                                               vse_sestavine=vse_sestavine)

@bottle.get('/dodaj-recept')
def dodaj_recept_get():
    return bottle.template('views/dodaj_recept.tpl', recept = model.ReceptPosSes(), kategorija=kategorije)

@bottle.post('/dodaj-recept')
def dodaj_recept_post():
    ime = str(bottle.request.forms.getunicode('ime'))
    st_porcij = int(bottle.request.forms.getunicode('st_porcij'))
    cas_priprave = int(bottle.request.forms.getunicode('cas_priprave'))
    cas_kuhanja = int(bottle.request.forms.getunicode('cas_kuhanja'))
    kategorija = str(bottle.request.forms.getunicode('ime_kategorije'))
    kulinarika = str(bottle.request.forms.getunicode('kulinarika'))
    oznaka = str(bottle.request.forms.getunicode('oznaka'))

    recept = r.dodaj_recept(model.Recepti(
        ime = ime,
        st_porcij=st_porcij,
        cas_priprave=cas_priprave,
        cas_kuhanja=cas_kuhanja
    ))

    r.dodaj_kategorijo(model.Kategorije(
        id_recepta=recept.id,
        kategorija=kategorija
    ))

    r.dodaj_kulinariko(model.Kulinarike(
        id_recepta=recept.id,
        kulinarika=kulinarika
    ))

    r.dodaj_oznako(model.Oznake(
        id_recepta=recept.id,
        oznaka = oznaka
    ))

    bottle.redirect('/recept/{}'.format(recept.id))


@bottle.post('/izbrisi-recept')
def izbrisi_recept():
    id = bottle.request.forms.getunicode('recept')
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    bottle.redirect('/')

@bottle.post('/izbrisi-recept/<id>')
def izbrisi_recept_id(id):
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(recept)
    bottle.redirect('/')


@bottle.post('/dodaj-sestavino/<id>')
def dodaj_sestavino(id):
    sestavina = str(bottle.request.forms.getunicode('dodana-sestavina'))
    enota =  str(bottle.request.forms.getunicode('dodana-enota'))
    kolicina =  str(bottle.request.forms.getunicode('dodana-kolicina'))

    r.dodaj_sestavino(model.SestavineReceptov(
            id_recepta=id,
            sestavina=sestavina,
            kolicina=kolicina,
            enota=enota
        ))

    nutrienti = r.dobi_nutrientske_vrednosti(id)
    s = model.SestavineReceptov(int(id), kolicina, enota, sestavina)
    r.pristej_nutriente(nutrienti, s)

    bottle.redirect('/recept/{}'.format(id))


@bottle.post('/dodaj-postopek/<id>')
def dodaj_postopek_post(id):
    postopek =  str(bottle.request.forms.getunicode('dodan-postopek'))
    vsi_koraki = r.dobi_vse_gen_id(model.Postopki, id, "id_recepta")
    zadnji_korak = max([x.st_koraka for x in vsi_koraki])

    r.dodaj_postopek(model.Postopki(
        id_recepta=id,
        postopek=postopek,
        st_koraka=zadnji_korak + 1
    ))
    bottle.redirect('/recept/{}'.format(id))



bottle.run(reloader=True, debug=True)