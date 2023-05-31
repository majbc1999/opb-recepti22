<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Recepti</title>

        <style>
            body {
              font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
              font-weight: normal;
            }

            
            .gumb {
              align-items: center;
              width: 100%;
              border: none;
              border-radius: 5px;
              background-color: whitesmoke;
              cursor: pointer;
              height: 2.5em;
              justify-content: center;
              line-height: 1.5;
              padding: calc(.5em - 1px) 1em;
            }
            .gumb:hover {
              border-color: #b5b5b5;
              border-radius: 5px;
              box-shadow: 2px 0px 7px 5px rgba(0,0,0,0.24),3px 0px 11px 7px rgba(0,0,0,0.19)
            }

            .gumb-moji-recepti {
              border: none;
              background-color: none;
            }
            .gumb-dodaj{
                width: inherit;
                margin-top: 80px;
                background-color:rgb(172, 201, 204);
            }
            .gumb-izbrisi {
                width: inherit;
                margin-top: 80px;
                background-color:rgb(204, 172, 172);
            }
            .gumb-sestavina {
              margin-top: 5px;
              margin-left: 15%;
              width: 70%;
            }
            .gumb-postopek {
              margin-top: 5px;
              margin-left: 25%;
              width: 50%;
            }
            .gumb-kategorije {
              margin-top: 10px;
              width: 2cm
            }


            .tabela{
                margin-left: auto;
                margin-right: auto;
            }
            .dodaj_tabela{
              width: 40%;
              margin-left: auto;
              margin-right: auto;
            }
            .prva-vrstica td {
                background-color: gainsboro;
                padding: 5px 10px;
                text-align: center;
            }
            .vrstica td {
                background-color: whitesmoke;
                text-align: center;
            }


            .okvir {
              position: absolute;
              top: 180px;
              right: 2%;
              border: solid gainsboro;
              border-radius: 10px;
              padding: 0 10px;
            }


            h1 {
                text-align: center;
                font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                margin-bottom: 1%;
                margin-top: 100px;
            }
            h2 {
                text-align: center;
                font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                margin-bottom: 2px;
            }
            h3 {
                text-align: left;
                font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                margin-bottom: 2px;
                padding: 4px;
                border-radius: 3px;
                color: white;
                background-color: dimgray;
            }
            .naslov {
                display: flex;
                justify-content: space-between;
                margin-left: 46.5%; 
                margin-right: 28%;
            }
            .mali-tisk {
              color: darkgray;
              font-size: small;
              margin-bottom: 0;
              margin-top: 35px;
            }


            .podatki {
              background-color: whitesmoke;
              border-radius: 3px;
              border-color: rgb(226, 223, 223);
              margin-top: 3px;
              margin-bottom: 0;
              padding: 2px;
            }
            .sestavine {
              width: 15%;
              position: absolute;
              left: 5%;
              top: 167px;
            }
            .postopek {
              width: 40%;
              margin-right: auto;
              margin-left: auto;
              padding: 8px;
            }


            .navigacija {
                font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                color: black;
                padding: 15px;
                width: 100%;
                top: 0;
                left: 0;
                position: fixed;
                background-color:rgb(117, 117, 117);
                z-index: 1000;
            }
            .nav-stolpec-1 {
                text-align: left;
                width: 26%;
                color: white;
            }
            .nav-stolpec-mid {
                width: 16%;
            }


            .dropdown {
              position: relative;
              padding: 0px 0px;
              margin: 2px 0;
              cursor: pointer;
            }
            .dropdown-content {
              font:small;
              display: none;
              position: absolute;
              width: 100%;
              overflow: auto;
              box-shadow: 0px 3px 3px 0px rgba(0,0,0,0.4);
              background-color: white;
              border-radius: 5px;
            }
            .dropdown:hover .dropdown-content {
              display: block;
            }
            .dropdown-content a {
              font-family: Arial, Helvetica, sans-serif;
              font-weight: normal;
              display: inline-block;
              color: #000000;
              padding: 1x;
              text-decoration: none;
            }
            .dropdown-content a:hover {
              color: #FFFFFF;
              background-color:indianred;
              width: 100%;
            }


            .dodaj-sestavino {
              margin-top: 5px;
              padding-left: 10px;
              width: 97%;
              height: 25px;
              border-radius: 5px;
            }
            .dodaj-postopek {
              margin-top: 5px;
              width: 100%;
              border-radius: 5px;
            }
            .izbira {
              width: fit-content; 
              background-color: white;
            }

            .v-vrsto {
              display: flex;
              justify-content: space-evenly;
            }

        
        </style>
    </head>
    <body>
        {{!base}}
    </body>
</html>