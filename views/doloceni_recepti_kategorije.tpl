<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Recepti</title>
</head>

<body>
    {{kategorija}}

    <table>
        % for recept in recepti:
            <tr>
                <td>
                    <form action='/{{recept.id}}/' method="POST">
                        <button type="submit">{{recept.ime}}</button> 
                    </form>
                </td>
                <td>{{recept.st_porcij}}</td>
                <td>{{recept.cas_priprave}}</td>
                <td>{{recept.cas_kuhanja}}</td>
            </tr>
        %end
    </table>            
</body>