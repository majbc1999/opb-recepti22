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
        <p><h3>Res želite izbrisati recept?:</h3></b>
            <div style="border-style: ridge; background-color: lightgoldenrodyellow; padding: 10px; width: fit-content;" class="panel-block">
                <form action="/izbrisi-recept/{{id}}" method="POST">
                    <p><input type="submit" value="Da izbrisi!" href='/'></p>
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
