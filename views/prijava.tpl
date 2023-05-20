<!DOCTYPE html>
<html>
    <form action="/prijava" method="POST" style="width:60%">
    <div class="form-group">
      <label for="username">Uporabniško ime</label>
      <input type="input" class="form-control" name="username"  placeholder="Vnesi uporabniško ime">
    </div>
    <div class="form-group">
      <label for="password">Geslo</label>
      <input type="password" class="form-control" name="password" placeholder="Geslo">
    </div>
   
    <button type="submit" class="btn btn-primary">Prijava</button>
    </form>

    %if napaka:
        <p class="opozorilo">{{napaka}}</p>
    %end
</html>