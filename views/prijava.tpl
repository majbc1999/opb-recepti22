% rebase('osnova.tpl')

<div class="center prijava" style="width:40%">
<h2>Prijava</h2>

  <form action="{{url('prijava')}}" method="POST" class="center" style="width:70%;">

    <label for="uporabnisko_ime">Uporabniško ime</label><br>
    <input type="input" class="dodaj-sestavino" name="uporabnisko_ime"  placeholder="Vnesi uporabniško ime">

    <label for="geslo">Geslo</label><br>
    <input type="password" class="dodaj-sestavino" name="geslo" placeholder="Geslo">

    <button type="submit" class="gumb gumb-sestavina">Prijava</button>
  </form>

  %if napaka:
      <p class="opozorilo">{{napaka}}</p>
  %end

  <p>Še niste registrirani?</p>
  <form action="{{url('registracija')}}" method="GET">
    <button type="submit" class="gumb">Registracija</button>
  </form>
</div>
