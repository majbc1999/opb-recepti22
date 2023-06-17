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
                </div>
            </div>
        </th>
    </tr>
</table>

<div class="naslov center">
    <h1>RECEPTI</h1>
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

        </tr>
    %end
</table>  
