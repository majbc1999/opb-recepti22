% rebase('osnova.tpl')

<div class="center prijava" style="width: 40%;">
  <h2>Registracija</h2>
  
    <form action="{{url('registracija')}}" method="POST" class="center" style="width:90%">
    
      <label for="uporabnisko_ime">Uporabniško ime</label><br>
      <input type="input" class="dodaj-sestavino" name="uporabnisko_ime"  placeholder="Vnesi uporabniško ime">

      <label for="geslo">Geslo</label><br>
      <input type="password" class="dodaj-sestavino" name="geslo" placeholder="Geslo">
   
    <button type="submit" class="gumb gumb-sestavina">Registracija</button>
    </form>

    %if napaka:
        <p class="opozorilo">{{napaka}}</p>
    %end
</div>