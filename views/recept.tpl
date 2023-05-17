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
    <div class="level-right">
        <p>Kliknite <a class="button is-primary" href="/izbrisi-recept/{{id}}" method="POST">TU</a>, če želite izbrisati recept.<br>
    </div>
    <div class="level-right">
        <p>Kliknite <a class="button is-primary" href="/dodaj-sestavino/{{id}}" method="POST">TU</a>, če želite dodati sestavino.<br>
    </div>
    <div class="level-right">
        <p>Kliknite <a class="button is-primary" href="/dodaj-postopek/{{id}}" method="POST">TU</a>, če želite dodati postopek.<br>
    </div>

</body>