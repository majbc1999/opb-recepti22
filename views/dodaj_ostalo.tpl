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

<div class='recept'>
    <h2 style="text-align: center;">DODAJ RECEPT</h2>
        <table class"dodaj_tabela" style="width=70%"> 
            <tr> <th>Ime recepta:</th> <td>{{recept.ime}}</td></tr>
            <tr> <th>Stevilo porcij:</th> <td>{{recept.st_porcij}}<td></tr>
            <tr> <th>Cas kuhanja:</th> <td>{{recept.cas_kuhanja}}<td></tr>
            <tr> <th>Cas priprave:</th> <td>{{recept.cas_priprave}}<td></tr>
        </table> 
</div>


<div class="postopek">
    <h2 style="text-align: left;">POSTOPEK</h2>
    <p class="mali-tisk">Izpolni spodnjo predlogo, da dodaš korak postopka.</p>
    <form action="/dodaj-prvi-postopek/{{recept.id}}" method="POST">
        <textarea name="dodan-postopek" class="dodaj-postopek" rows="3" cols="90" placeholder="Postopek" required></textarea>
        <button class="gumb gumb-postopek" type="submit" >Dodaj korak</button>
    </form>
</div>
    

<div class="sestavine">
    <h2>SESTAVINE</h2>

    <p class="mali-tisk">Izpolni spodnjo predlogo, da dodaš sestavino.</p>
    <form action="/dodaj-prvo-sestavino/{{recept.id}}" method="POST">
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



<div class="postopek" style="margin-top: 50px;">
<h3>Izberite označbe, ki jih želite dodati.</h3>

<div class="v-vrsto">
<form action="/dodaj-prvo-kategorijo/{{recept.id}}" method="POST">
        % for kategorija in [k for k in kategorije if k not in kategorije_recepta]:
            <input type="checkbox" id="kategorija" name="kategorija" value="{{kategorija}}">
            <label for="kategorija">{{kategorija}}</label><br>
        % end
    </select>
    <button class="gumb gumb-kategorije" type="submit" >Dodaj</button>
</form>

<form action="/dodaj-prvo-kulinariko/{{recept.id}}" method="POST">
        % for kulinarika in [k for k in kulinarike if k not in kulinarike_recepta]:
            <input type="checkbox" id="kulinarika" name="kulinarika" value="{{kulinarika}}">
            <label for="kulinarika">{{kulinarika}}</label><br>
        % end
    </select>
    <button class="gumb gumb-kategorije" type="submit" >Dodaj</button>
</form>

<form action="/dodaj-prvo-oznako/{{recept.id}}" method="POST">
    <div style="overflow-y: scroll; height:595px;">
        % for oznaka in [k for k in oznake if k not in oznake_recepta]:
            <input type="checkbox" id="oznaka" name="oznaka" value="{{oznaka}}">
            <label for="oznaka">{{oznaka}}</label><br>
        % end
    </select>
    </div>
    <button class="gumb gumb-kategorije" type="submit">Dodaj</button>
</form>
</div>
</div>
    



    



