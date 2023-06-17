% rebase('osnova.tpl')

<table class="navigacija">
    <tr>
        <th class="nav-stolpec-1">
            <form action="/moji-recepti" method="GET">
                <button class="gumb-moji-recepti" type="submit">Moji recepti</button>
            </form>
        </th>
        <th class="nav-stolpec-1">
            <form action="/recepti" method="GET">
                <button class="gumb-moji-recepti" type="submit">Vsi recepti</button>
            </form>
        </th>
        <th class="nav-stolpec-1"></th>
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
        <th class="nav-stolpec-1"></th>
        <th class="nav-stolpec-1"></th>
        <th class="nav-stolpec-1">
            <div class="dropdown" style="text-align: center;">
                ° ° °
                <div class="dropdown-content">
                    <div class="button">
                        <a class="button" href="/prijava" method="GET">Prijava</a><br>
                    </div>
                    <div class="button">
                        <a class="button" href="/odjava" method="POST">Odjava</a><br>
                    </div>
                </div>
            </div>
        </th>
    </tr>
</table>

<div class='recept'>
    <h1>DODAJ RECEPT</h1>
        <table class="dodaj_tabela" style="width:70%"> 
            <tr>
                <td>Ime recepta:{{recept.ime}}</td>
                <td>Stevilo porcij:{{recept.st_porcij}}</td>
                <td>Cas kuhanja:{{recept.cas_kuhanja}}</td>
                <td>Cas priprave:{{recept.cas_priprave}}</td>
            </tr>
        </table> 
</div>


<div class="flex-container">

    <div>
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
                <td>
                    <form action="/izbrisi-sestavino/{{recept.id}}" method="POST">
                        <button class="gumb" name="sestavina" value="{{sestavina.sestavina}}" type="submit">Izbriši</button>
                    </form>
                </td>
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

    <div>
        <h2 style="text-align: left;">POSTOPEK</h2>
        <table class="tabela" id="postopek">
            % for korak in postopek:
            <tr class="vrstica">
                <td style="padding: 3px 7px;">{{korak.st_koraka}}</td>
                <td style="text-align: left;padding: 3px 7px;">{{korak.postopek}}</td>
                <td>
                    <form action="/izbrisi-postopek/{{recept.id}}" method="POST">
                        <button class="gumb" name="korak" value="{{korak.postopek}}" type="submit">Izbriši</button>
                    </form>
                </td>
                <td>
                    <input type="button" class="gumb" name="answer" value="Uredi" onclick="showDiv()" />
                    <script>
                        function showDiv() {
                           document.getElementById('welcomeDiv').style.display = "block";
                        }
                    </script>
                </td>
            </tr>
            <tr>
                <div id="welcomeDiv"  style="display:none; margin-bottom: 15px;" class="answer_list" >
                    <p class="mali-tisk">Uredi korak #{{korak.st_koraka}}</p>
                    <form action="/uredi-postopek/{{recept.id}}" method="POST">
                        <textarea name="spremenjen-postopek" class="dodaj-postopek" rows="2" cols="90" placeholder="{{korak.postopek}}" required>{{korak.postopek}}</textarea>
                        <button class="gumb gumb-postopek" name="nov_korak" value="{{korak.st_koraka}}" type="submit">Končaj urejanje</button>
                    </form>
                </div>
            </tr>
            % end
        </table>

        <p class="mali-tisk">Izpolni spodnjo predlogo, da dodaš korak postopka.</p>
        <form action="/dodaj-postopek/{{recept.id}}" method="POST">
            <textarea name="dodan-postopek" class="dodaj-postopek" rows="3" cols="90" placeholder="Postopek" required></textarea>
            <button class="gumb gumb-postopek" type="submit" >Dodaj korak</button>
        </form>
    </div>


    <div class="okvir">
        <h3>NUTRIENTSKE VREDNOSTI</h3>
        <p class="podatki" style="margin-bottom: 0;">Kalorije: {{nutrientske_vrednosti.kalorije}} Cal</p>
        <p class="podatki" style="margin-bottom: 0;">Ogljikovi hidrati: {{nutrientske_vrednosti.ogljikovi_hidrati}} g</p>
        <p class="podatki" style="margin-bottom: 0;">Maščobe: {{nutrientske_vrednosti.mascobe}} g</p>
        <p class="podatki" style="margin-bottom: 0;">Beljakovine: {{nutrientske_vrednosti.proteini}} g</p>

        <h3>KATEGORIJE</h3>
        % for kategorija in kategorije_recepta:
        <div class="podatki" style="display: flex;height: 25px;">
            <p style="flex:1;margin-top: 0;">{{kategorija}}</p>
            <form action="/izbrisi-kategorijo/{{recept.id}}" method="POST">
                <button class="gumb-link" name="kategorija" value="{{kategorija}}" type="submit">Izbriši</button>
            </form>
        </div>
        % end

        <h3>KULINARIKE</h3> 
        % for kulinarika in kulinarike_recepta:
        <div class="podatki" style="display: flex;height: 25px;">
            <p style="flex:1;margin-top: 0;">{{kulinarika}}</p>
            <form action="/izbrisi-kulinariko/{{recept.id}}" method="POST">
                <button class="gumb-link" name="kulinarika" value="{{kulinarika}}" type="submit">Izbriši</button>
            </form>
        </div>
        % end

        <h3>OZNAKE</h3>
        % for oznaka in oznake_recepta:
        <div class="podatki" style="display: flex;height: 25px;">
            <p style="flex:1;margin-top: 0;">{{oznaka}}</p>
            <form action="/izbrisi-oznako/{{recept.id}}" method="POST">
                <button class="gumb-link" name="oznaka" value="{{oznaka}}" type="submit">Izbriši</button>
            </form>
        </div>
        % end
    </div>
</div>

<div class="center" style="margin-top: 50px; width: 50%;">
<h3>Izberite označbe, ki jih želite dodati.</h3>

<div class="v-vrsto">
<form action="/dodaj-kategorijo/{{recept.id}}" method="POST">
    <h3>Kategorije</h3>
        % for kategorija in [k for k in kategorije if k not in kategorije_recepta]:
            <input type="checkbox" id="kategorija" name="kategorija" value="{{kategorija}}">
            <label for="kategorija">{{kategorija}}</label><br>
        % end
    <button class="gumb gumb-kategorije" type="submit" >Dodaj</button>
</form>

<form action="/dodaj-kulinariko/{{recept.id}}" method="POST">
    <h3>Kulinarike</h3>
        % for kulinarika in [k for k in kulinarike if k not in kulinarike_recepta]:
            <input type="checkbox" id="kulinarika" name="kulinarika" value="{{kulinarika}}">
            <label for="kulinarika">{{kulinarika}}</label><br>
        % end
    </select>
    <button class="gumb gumb-kategorije" type="submit" >Dodaj</button>
</form>

<form action="/dodaj-oznako/{{recept.id}}" method="POST">
    <h3>Oznake</h3>
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


<div id="footer">
    <form action="/recepti" method="GET">
        <div class="center" style="width:40%">    
            <button class="gumb gumb-kategorije" type="submit">Končano</a>
        </div>
    </form>
</div>

