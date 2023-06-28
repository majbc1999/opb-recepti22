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



<div class="naslov center" style="color: darkred;">
    <h1>{{recept.ime}}</h1>
</div>

<div class="flex-container">
    <div>
        <h2>SESTAVINE</h2>
        <table class="tabela" id="sestavine_recepta">
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
    </div>
    
    <div>
        <h2 style="text-align: center;">POSTOPEK</h2>
        <table class="tabela" id="postopek">
            % for korak in postopek:
            <tr class="vrstica">
                <td style="padding: 3px 7px;">{{korak.st_koraka}}</td>
                <td style="text-align: left;padding: 3px 7px;">{{korak.postopek}}</td>
            </tr>
            % end
        </table>
    </div>

    <div class="okvir">
        <h3>NUTRIENTSKE VREDNOSTI</h3>
        <p class="podatki" style="margin-bottom: 0;">Kalorije: {{nutrientske_vrednosti.kalorije}} Cal</p>
        <p class="podatki" style="margin-bottom: 0;">Ogljikovi hidrati: {{nutrientske_vrednosti.ogljikovi_hidrati}} g</p>
        <p class="podatki" style="margin-bottom: 0;">Maščobe: {{nutrientske_vrednosti.mascobe}} g</p>
        <p class="podatki" style="margin-bottom: 0;">Beljakovine: {{nutrientske_vrednosti.proteini}} g</p>

        <h3>KATEGORIJE</h3>
        % for kategorija in kategorije_recepta:
        <p class="podatki">{{kategorija}}</p>
        % end

        <h3>KULINARIKE</h3> 
        % for kulinarika in kulinarike_recepta:
        <p class="podatki">{{kulinarika}}</p>
        % end

        <h3>OZNAKE</h3>
        % for oznaka in oznake_recepta:
        <p class="podatki">{{oznaka}}</p>
        % end
    </div>
</div>



<h2 style="text-align: center;">KOMENTARJI</h2>

<p class="mali-tisk">Pustite komentar.</p>
<form action="/dodaj-komentar/{{recept.id}}" method="POST">
    <textarea name="dodan-komentar" class="dodaj-postopek" rows="3" cols="90" placeholder="Komentar" required></textarea>
    <button class="gumb gumb-postopek" type="submit" >Objavi</button>
</form>


<table class="center" style="width: 60%;">
    % for komentar in slovarji_komentarjev:
    <tr>
        <td class="komentar">
            <div style="color: gray;">{{komentar['ime_uporabnika']}} -- {{komentar['datum_objave']}}</div><br>
            {{komentar['vsebina']}}
        </td>
    </tr>
    % end
</table>