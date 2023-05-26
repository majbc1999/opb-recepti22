%rebase(osnova.tpl)

<body>
    {{kategorija}}

    <form method="POST">
    <div style="margin: 10%;">
        <p><h3>Dodaj recept:</h3></b>
            <div style="border-style: ridge; background-color: lightgoldenrodyellow; padding: 10px; width: fit-content;" class="panel-block">
                <form action="/dodaj-recept" method="POST">
                    Ime recepta: <input type="text" name="ime">
                    Stevilo porcij: <input type="int" name="st_porcij">
                    Cas kuhanja: <input type="int" name="cas_kuhanja">
                    Cas priprave: <input type="int" name="cas_priprave">
                    Ime kategorije: <input type="text" name="ime_kategorije">
                    Kulinarika: <input type="text" name="kulinarika">
                    Oznaka: <input type="text" name="oznaka">
                    <p><input type="submit" value="Dodaj recept!" href="/"></p>
                </form>
            </div>
    </div>
    <div id="footer">
        <div class="control">
            <a class="button is-link is-light" href="/">Prekliči</a>
        </div>
    </div>
    </form>
</body>
