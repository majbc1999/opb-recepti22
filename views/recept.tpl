% rebase('osnova.tpl')

<table class="navigacija">
    <tr>
        <th class="nav-stolpec-1">
            Moji recepti
        </th>
        <th class="nav-stolpec-mid">
            <div class="dropdown">
                Kategorije
                <div class="dropdown-content">
                    % for kategorija in kategorije:
                        <a href="/recepti-kategorije/{{kategorija}}">{{kategorija}}</a><br>
                    % end
                </div>
            </div>
        </th>
        <th class="nav-stolpec-mid">
            <div class="dropdown">
                Kulinarike
                <div class="dropdown-content">
                    % for kulinarika in kulinarike:
                        <a href="/recepti-kulinarike/{{kulinarika}}">{{kulinarika}}</a><br>
                    % end
                </div>
            </div>
        </th>
        <th class="nav-stolpec-mid">
            <div class="dropdown">
                Oznake
                <div class="dropdown-content" style="height: 500px;">
                    % for oznaka in oznake:
                        <a href="/recepti-oznake/{{oznaka}}">{{oznaka}}</a><br>
                    % end
                </div>
            </div>
        </th>
        <th></th>
    </tr>
</table>

<div class="naslov postopek" style="color: darkred;">
    <h1>{{recept.ime}}</h1>
    
    <form action="/izbrisi-recept/{{recept.id}}" method="POST">
        <button class="gumb gumb-izbrisi" type="submit">Izbriši</button>
    </form>
</div>
	

<div class="postopek">
    <h2 style="text-align: left;">POSTOPEK</h2>
    <table class="tabela" id="postopek">
        % for korak in postopek:
        <tr class="vrstica">
            <td style="padding: 3px 7px;">{{korak.st_koraka}}</td>
            <td style="text-align: left;padding: 3px 7px;">{{korak.postopek}}</td>
        </tr>
        % end
    </table>

    <p class="mali-tisk">Izpolni spodnjo predlogo, da dodaš korak postopka.</p>
    <form action="/dodaj-postopek/{{recept.id}}" method="POST">
        <textarea name="dodan-postopek" class="dodaj-postopek" rows="3" cols="90" placeholder="Postopek" required></textarea>
        <button class="gumb gumb-postopek" type="submit" >Dodaj korak</button>
    </form>
</div>
    

<div class="sestavine">
    <h2>SESTAVINE</h2>
    <table class="tabela" id="sestavine_recepta" style="width:100%">
        <tr class="prva-vrstica">
            <td>sestavina</td>
            <td>količina</td>
        </tr>
        % for sestavina in sestavine_recepta:
        <tr class="vrstica">
            <td style="text-align: left; padding-left: 8px;">{{sestavina.sestavina}}</td>
            <td>{{sestavina.kolicina}} {{sestavina.enota}}</td>
        </tr>
        % end
    </table>

    <p class="mali-tisk">Izpolni spodnjo predlogo, da dodaš sestavino.</p>
    <form action="/dodaj-sestavino/{{recept.id}}" method="POST">
        <datalist id="vse_sestavine">
            % for sestavina in vse_sestavine:
            <option>{{sestavina.ime}}</option>
            %end
        </datalist>
        <input name="dodana-sestavina" class="dodaj-sestavino" autocomplete="on" list="vse_sestavine" placeholder="Sestavina" required/>

        <input name="dodana-kolicina" class="dodaj-sestavino" type="number" placeholder="Količina" step="0.01" required>

        <label for="enota">Enota:</label>
        <select class="dodaj-sestavino izbira" name="dodana-enota" id="enota">
            <option value="g">g</option>
            <option value="ml">ml</option>
            <option value="cup">cup</option>
            <option value="cup">ounce</option>
            <option value="cup">pound</option>
            <option value="cup">tbsp</option>
            <option value="cup">tsp</option>
            <option value="cup">bunch</option>
            <option value="cup">scoop</option>
            <option value="cup">egg</option>
        </select>

        <button class="gumb gumb-sestavina" type="submit" >Dodaj sestavino</button>
    </form>
</div>


<div class="okvir" style="margin-right: 15px;">
    <h3>NUTRIENTSKE VREDNOSTI</h3>
    <p class="podatki" style="margin-bottom: 0;">Kalorije: {{nutrientske_vrednosti.kalorije}} Cal</p>
    <p class="podatki" style="margin-bottom: 0;">Ogljikovi hidrati: {{nutrientske_vrednosti.ogljikovi_hidrati}} g</p>
    <p class="podatki" style="margin-bottom: 0;">Maščobe: {{nutrientske_vrednosti.mascobe}} g</p>
    <p class="podatki" style="margin-bottom: 0;">Beljakovine: {{nutrientske_vrednosti.proteini}} g</p>
    
    <h3>KATEGORIJE</h3>
    % for kategorija in kategorije_recepta:
    <p class="podatki">{{kategorija.kategorija}}</p>
    % end
    
    <h3>KULINARIKE</h3> 
    % for kulinarika in kulinarike_recepta:
    <p class="podatki">{{kulinarika.kulinarika}}</p>
    % end
    
    <h3>OZNAKE</h3>
    % for oznaka in oznake_recepta:
    <p class="podatki" style="margin-bottom: 0;">{{oznaka.oznaka}}</p>
    % end
</div>
    
    