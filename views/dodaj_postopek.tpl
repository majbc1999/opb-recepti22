<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Recepti</title>
</head>

<body>

    <form method="POST">
    <div style="margin: 10%;">
        <p><h3>Dodaj postopek:</h3></b>
            <div style="border-style: ridge; background-color: lightgoldenrodyellow; padding: 10px; width: fit-content;" class="panel-block">
                <form action="/dodaj-postopek/{{id}}" method="POST">
                    Korak postopka: <input type="text" name="postopek">
                    Stevilo koraka: <input type="int" name="st_koraka">
                    <p><input type="submit" value="Dodaj postopek!" href='/recept/{{id}}'></p>
                </form>
            </div>
    </div>
    <div id="footer">
        <div class="control">
            <a class="button is-link is-light" href='/'>Prekliči</a>
        </div>
    </div>
    </form>
</body>
