<template>
     <div class="container">
        <p class="h3 my-5">Unesite infromacije o kolima</p>
        <form>
            <div class="form-group my-3">
                <label for="adresaVozila">Gde se Vaše vozilo nalazi?</label>
                <input type="text" class="form-control" id="adresaVozila" placeholder="Unesite adresu" required>
            </div>
            <div class="input-group">                
                <div class="form-group my-3 mr-3">
                    <label for="godinaProizvodnje">Godina proizvodnje</label>
                    <input type="number" min="1900" max = "2099" step="1" value="2022" class="form-control" id="godinaProzvodnje" required>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="marka">Marka</label>
                    <input type="text" class="form-control" id="marka" placeholder="Marka" required>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Model</label>
                    <input type="text" class="form-control" id="model" placeholder="Model" required>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Kilometraža</label>
                    <select class="form-select" aria-label="Izaberite raspon" required>
                        <option selected disabled>Izaberi</option>
                        <option value="1">0-20k km</option>
                        <option value="2">20-40k km</option>
                        <option value="3">40-60k km</option>
                        <option value="4">60-80k km</option>
                        <option value="5">80-100k km</option>
                        <option value="6">100-120k km</option>
                        <option value="7">120-140k km</option>
                        <option value="8">140-160k km</option>
                        <option value="9">160-180k km</option>
                        <option value="10">180-200k km</option>
                        <option value="11">200k+ km</option>
                      </select>
                </div>
            </div>
            <div class="form-group my-3">
                <label for="">Tip transmisije</label>
                <div class="d-flex">
                    <div class="form-check mx-3">
                        <label for="manual">Manual</label>
                        <input class="form-check-input form-control" type="radio" id="manual" name ="menjac" checked>
                    </div>
                    <div class="form-check mx-3">
                        <label for="automatik">Automatik</label>
                        <input class="form-check-input form-control" type="radio" id="automatik" name="menjac">
                    </div>
                </div>
                
            <div class="input-group">
                <div class="form-group my-3 mr-3">
                    <label for="model">Tip vozila</label>
                    <select class="form-select" aria-label="Izaberite" required>
                        <option selected disabled>Izaberi</option>
                        <option value="1">Sedan</option>
                        <option value="2">Kupe</option>
                        <option value="3">Kabriolet</option>
                        <option value="4">Karavan</option>
                        <option value="5">SUV</option>
                        <option value="6">Kombi</option>
                        <option value="7">Kamion</option>
                    </select>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Gorivo</label>
                    <select class="form-select" aria-label="Izaberite" required>
                        <option selected disabled>Izaberi</option>
                        <option value="1">Dizel</option>
                        <option value="2">Benzin</option>
                        <option value="3">Hibrid</option>
                        <option value="4">Električni</option>
                    </select>
                </div>
                <div class="form-group my-3 mx-3">
                    <div class="input-group">
                        <label for="model">Cena po danu (u &euro;): </label> <input type="number" min="10" max = "205" class="form-control mx-3" size="3" id="rangeVal">
                    </div>
                    <input type="range" class="form-range mt-2" min="10" max="205" id="customRange2" required>
                </div>
            </div>

            </div>
            
            <div class="form-group my-3">
                <label for="exampleFormControlTextarea1" class="mb-1">Slike vozila</label> <br>
                <input type="file" id="car-photo" name="car-photo" accept="image/png, image/jpeg" multiple required>
            </div>
            <div class="form-group">
              <label for="opis-kola">Opis vozila</label>
              <textarea class="form-control" id="opis-kola" rows="5" required></textarea>
            </div>
            <div class="form-group my-3">
                <input type="submit" class="btn btn-dark"  value="Pošalji">
            </div>
        </form>
    </div>
</template>