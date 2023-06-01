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
        <th class="nav-stolpec-mid">
            <div class="button">
                <a class="button is-link is-light" href="/odjava" method="POST">Odjava</a><br>
            </div>
        </th>
        <th></th>
    </tr>
</table>

<div class='recept'>
    <h1>1. KORAK</h1>
    <div class="dodaj_tabela">
        <form action="/dodaj-recept" method="POST">
            <table style="width:40%;"> 
                <tr> <th>Ime recepta:</th> <td><input type="text" name="ime"></td></tr>
                <tr> <th>Stevilo porcij:</th> <td><input type="number" name="st_porcij"><td></tr>
                <tr> <th>Cas kuhanja:</th> <td><input type="number" name="cas_kuhanja"><td></tr>
                <tr> <th>Cas priprave:</th> <td><input type="number" name="cas_priprave"><td></tr>
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




    



