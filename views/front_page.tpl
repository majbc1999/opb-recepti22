<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link rel="stylesheet" href="C:\Lucija\1.letnik fmf\UVP\nutrient-tracker\views\style.css" type='text/css/'> -->
        <title>Recepti</title>

        <style>
            .dropdown {
              display: inline-block;
              position: relative;
            }
            .dropdown-content {
              display: none;
              position: absolute;
              width: 100%;
              overflow: auto;
              box-shadow: 0px 10px 10px 0px rgba(0,0,0,0.4);
            }
            .dropdown:hover .dropdown-content {
              display: block;
            }
            .dropdown-content a {
              display: block;
              color: #000000;
              padding: 5px;
              text-decoration: none;
            }
            .dropdown-content a:hover {
              color: #FFFFFF;
              background-color: #00A4BD;
            }
        </style>
</head>

<body>
    <table id="header">
        <tr>
            <th>
                <div class="dropdown">
                    <button>Kategorije</button>
                    <div class="dropdown-content">
                        % for kategorija in kategorije:
                            <a href="/recepti-kategorije/{{kategorija}}">{{kategorija}}</a>
                        % end
                    </div>
                </div>
            </th>
            <th>
                <div class="dropdown">
                    <button>Kulinarike</button>
                    <div class="dropdown-content">
                        % for kulinarika in kulinarike:
                            <a href="/recepti-kulinarike/{{kulinarika}}">{{kulinarika}}</a>
                        % end
                    </div>
                </div>
            </th>
            <th>
                <div class="dropdown">
                    <button>Oznake</button>
                    <div class="dropdown-content">
                        % for oznaka in oznake:
                            <a href="/recepti-oznake/{{oznaka}}">{{oznaka}}</a>
                        % end
                    </div>
                </div>
            </th>
        </tr>
    </table>
</body>
</html>