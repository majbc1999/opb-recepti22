<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Recepti</title>
</head>
<body>
    {{id}}
    <div id="footer">
        <div class="control">
            <a class="button is-link is-light" href="/">Izhod</a>
        </div>
    </div>
    <form method="POST">
        <form action="/izbrisi-recept/{{id}}" method="POST">
        <div class="level-right">
            <p><input type="submit" value="Izbrisi recept!" href="/"></p>
        </div>
        </form>
    </form>
</body>