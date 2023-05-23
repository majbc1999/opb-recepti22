% rebase('osnova.tpl')

<table class="navigacija">
    <tr>
        <th class="nav-stolpec-1">
            <form action="/moji-recepti" method="GET">
                <button class="gumb-moji-recepti" type="submit">Moji recepti</button>
            </form>
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

<div class="naslov">
<h1>RECEPTI</h1>

<form action="/dodaj-recept" method="GET">
    <button class="gumb gumb-dodaj" type="submit">Dodaj nov recept</button>
</form>
</div>

<table class="tabela" id="recepti">
    <tr class="prva-vrstica">
        <td>ime recepta</td>
        <td>število porcij</td>
        <td>čas priprave</td>
        <td>čas kuhanja</td>
    </tr>
    % for recept in recepti:
        <tr class="vrstica">
            <td>
                <form action='/{{recept.id}}/' method="POST">
                    <button class="gumb" style="text-align: left;" type="submit">{{recept.ime}}</button> 
                </form>
            </td>
            <td>{{recept.st_porcij}}</td>
            <td>{{recept.cas_priprave}}</td>
            <td>{{recept.cas_kuhanja}}</td>
            <td>
                <form action="/urejanje-recepta/{{recept.id}}" method="GET">
                    <button class="gumb" type="submit">Uredi</button>
                </form>
            </td>
            <td>
                <form action="/izbrisi-recept" method="POST">
                    <button class="gumb" name="recept" value="{{recept.id}}" type="submit">Izbriši</button>
                </form>
            </td>
        </tr>
    %end
</table>  