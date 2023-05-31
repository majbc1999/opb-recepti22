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

<div class='recept'>
    <h1>DODAJ SESTAVINO</h1>
    <div class="dodaj_tabela">
        <form action="/dodaj-novo-sestavino" method="POST">
            <table style="width:40%;align=center"> 
                <tr> <th>Ime sestavine:</th> <td><input type="text" name="ime"></td></tr>
                <tr> <th>Kolicina kalorij:</th> <td><input type="number" name="kalorije"><td></tr>
                <tr> <th>Kolicina proteinov:</th> <td><input type="number" name="proteini"><td></tr>
                <tr> <th>Kolicina ogljikovih hidratorv:</th> <td><input type="number" name="ogljikovi-hidrati"><td></tr>
                <tr> <th>Kolicina mascob:</th> <td><input type="number" name="mascobe"><td></tr>
            </table>
        <button class="gumb gumb-recept" type="submit" >Dodaj</button>
        </form>
    </div>
</div>

<div id="footer">
    <div class="control">
        <a class="button is-link is-light" href='/recepti'>Prekliči</a>
    </div>
</div>