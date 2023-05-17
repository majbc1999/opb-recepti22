from operator import mod
import bottle 
import bottletext
import model
import Database

r = Database.Repo()
kategorije = [x.kategorija for x in r.dobi_razlicne_gen(model.Kategorije, 'kategorija', 181, 0)]
kulinarike = [x.kulinarika for x in r.dobi_razlicne_gen(model.Kulinarike, 'kulinarika', 181, 0)]
oznake = [x.oznaka for x in r.dobi_razlicne_gen(model.Oznake, 'oznaka', 181, 0)]


@bottle.get('/')
def front_page():
    return bottle.template('views/front_page.tpl', kategorije=kategorije,
                                                   kulinarike=kulinarike,
                                                   oznake=oznake)


@bottle.get('/recepti-kategorije/<kategorija>')
def doloceni_recepti(kategorija):
    seznam_idjev = r.dobi_gen_ime(model.Kategorije, kategorija, 'kategorija', 'id_recepta')
    recepti_izbrane_kategorije = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return bottle.template('views/doloceni_recepti_kategorije.tpl', kategorija=kategorija,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kategorije)

@bottle.get('/recepti-kulinarike/<kulinarika>')
def doloceni_recepti(kulinarika):
    seznam_idjev = r.dobi_gen_ime(model.Kulinarike, kulinarika, 'kulinarika', 'id_recepta')
    recepti_izbrane_kulinarike = [r.dobi_gen_id(model.Recepti, x.id_recepta,'id') for x in seznam_idjev]

    return bottle.template('views/doloceni_recepti_kulinarike.tpl', kulinarika=kulinarika,
                                                                    kategorije=kategorije,
                                                                    kulinarike=kulinarike,
                                                                    oznake=oznake,
                                                                    recepti=recepti_izbrane_kulinarike)

@bottle.get('/recepti-oznake/<oznaka>')
def doloceni_recepti(oznaka):
    seznam_idjev = r.dobi_gen_ime(model.Oznake, oznaka, 'oznaka', 'id_recepta')
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
    return bottle.template('views/recept.tpl', id=id,
                                               kategorije=kategorije,
                                               kulinarike=kulinarike,
                                               oznake=oznake)
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


@bottle.get('/izbrisi-recept/<id>')
def izbrisi_recept_get(id):
    return bottle.template('views/izbrisi_recept', id=id,
                                               kategorije=kategorije,
                                               kulinarike=kulinarike,
                                               oznake=oznake)

@bottle.post('/izbrisi-recept/<id>')
def izbrisi_recept_post(id):
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.brisi_recept(model.Recepti(
        id=id,
        ime= recept.ime,
        st_porcij=recept.st_porcij,
        cas_priprave=recept.cas_priprave,
        cas_kuhanja=recept.cas_kuhanja
    ))
    bottle.redirect('/')



@bottle.get('/dodaj-sestavino/<id>')
def dodaj_sestavino_get(id):
    return bottle.template('views/dodaj_sestavino.tpl', id=id,
                                               kategorije=kategorije,
                                               kulinarike=kulinarike,
                                               oznake=oznake)

@bottle.post('/dodaj-sestavino/<id>')
def dodaj_sestavino_post(id):
    kolicina =  str(bottle.request.forms.getunicode('kolicina'))
    enota =  str(bottle.request.forms.getunicode('enota'))
    sestavina = str(bottle.request.forms.getunicode('sestavine'))
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.dodaj_sestavino(model.SestavineReceptov(
        id_recepta=recept.id,
        kolicina=kolicina,
        enota=enota,
        sestavina=sestavina
    ))
    bottle.redirect('/recept/{}'.format(recept.id))



@bottle.get('/dodaj-postopek/<id>')
def dodaj_postopek_get(id):
    return bottle.template('views/dodaj_postopek.tpl', id=id,
                                               kategorije=kategorije,
                                               kulinarike=kulinarike,
                                               oznake=oznake)


@bottle.post('/dodaj-postopek/<id>')
def dodaj_postopek_post(id):
    postopek =  str(bottle.request.forms.getunicode('postopek'))
    st_koraka =  int(bottle.request.forms.getunicode('st_koraka'))
    recept = r.dobi_gen_id(model.Recepti, id, 'id')
    r.dodaj_postopek(model.Postopek(
        id_recepta=recept.id,
        postopek=postopek,
        st_koraka=st_koraka
    ))
    bottle.redirect('/recept/{}'.format(recept.id))



bottle.run(reloader=True, debug=True)