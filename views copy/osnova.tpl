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
              font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
              font-weight: bold;
              border: none;
              background: none;
              padding: 0 0;
              margin-top: 7px;
              width: 100%;
              height: 1cm;
              cursor: pointer;
            }
            .gumb-moji-recepti:hover {
              color: indianred;
            }

            .gumb-dodaj{
                width: 14%;
                height: inherit;
                position: absolute;
                margin-top: 80px;
                margin-bottom: 5px;
                background-color:rgb(172, 201, 204);
            }
            .gumb-izbrisi {
                right: 15%;
                position:absolute;
                width: inherit;
                margin-top: 85px;
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
            }
            .gumb-link {
              border: none;
              outline: none;
              background: none;
              cursor: pointer;
              color: #0000EE;
              padding: 0;
              text-decoration: underline;
              font-family: inherit;
              font-size: inherit;
              flex: 1;
              height: fit-content;
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


            h1 {
                text-align: center;
                font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
                margin-bottom: 1%;
                margin-top: 100px;
                margin-left: auto;
                margin-right: auto;
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

            .prijava {
              border: 3px solid indianred;
              border-radius: 9px;
              top: 100px;
            }


            .flex-container {
              display: flex;
              flex-wrap: nowrap;
              justify-content: center;
              align-items: stretch;
            }
            .flex-container > div {
              margin: 10px;
            }

            .okvir {
              border: solid gainsboro;
              border-radius: 10px;
            }
            .podatki {
              background-color: whitesmoke;
              border-radius: 3px;
              border-color: rgb(226, 223, 223);
              margin-top: 3px;
              margin-bottom: 0;
              padding: 2px;
              height: fit-content;
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
                width: 8%;
                color: white;
            }
            .nav-stolpec-mid {
                width: 17.3%;
            }


            .dropdown {
              position: relative;
              padding: 0px 0px;
              margin: 2px 0;
              cursor: pointer;
            }
            .dropdown-content {
              font:small;
              text-align: center;
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

            .komentar {
              background-color: rgb(247, 244, 244);
              border-color: darkgray;
              border-radius: 5px;
              text-align: left;
              margin-top: 5px;
              padding: 2%;
            } 

            .v-vrsto {
              display: flex;
              justify-content: space-evenly;
            }
            .center {
              margin: auto;
              padding: 10px;
            }

        
        </style>
    </head>
    <body>
        {{!base}}
    </body>
</html>