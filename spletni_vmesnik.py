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


bottle.run(reloader=True, debug=True)