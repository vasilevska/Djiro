<template>
     <div class="container">
         <form enctype="multipart/form-data" id="my-form">
        <p class="h3 my-5">Unesite infromacije o kolima</p>
            <div class="form-group my-3">
                <label for="adresaVozila">Gde se Vaše vozilo nalazi?</label>
                <input type="text" class="form-control" name="address" id="adresaVozila" placeholder="Unesite adresu" required>
            </div>
            <div class="input-group">                
                <div class="form-group my-3 mr-3">
                    <label for="godinaProizvodnje">Godina proizvodnje</label>
                    <input type="number" min="1900" max = "2099" step="1" value="2022" class="form-control" name="year" id="godinaProzvodnje" required>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="marka">Marka</label>
                    <!-- <input type="text" class="form-control" name="manufacturer" id="marka" placeholder="Marka" required> -->
                    <select class="form-select" aria-label="Izaberite proizvođаča" id="manafacturer" required>
                        <option value="Peugeot">Peugeot</option>
                        <option value="Volvo">Volvo</option>
                        <option value="Toyota">Toyota</option>
                        <option value="Suzuki">Suzuki</option>
                        <option value="Ford">Ford</option>
                        <option value="Jaguar">Jaguar</option>
                        <option value="Alpha Romeo">Alpha Romeo</option>
                        <option value="MINI">MINI</option>
                        <option value="Nissan">Nissan</option>
                        <option value="Porsche">Porsche</option>
                        <option value="Volkswagen">Volkswagen</option>
                        <option value="Škoda">Škoda</option>
                      </select>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Model</label>
                    <input type="text" class="form-control" name="model" id="model" placeholder="Model" required>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Kilometraža</label>
                    <input type="number" min="0" max = "1000000" step="1"  class="form-control" name="km" id="kilometraza" required>
                </div>
            </div>
            <div class="form-group my-3">
                <label for="">Tip transmisije</label>
                <div class="d-flex">
                    <div class="form-check mx-3">
                        <label for="manual">Manual</label>
                        <input class="form-check-input form-control" type="radio" id="manual" name ="transmission" checked>
                    </div>
                    <div class="form-check mx-3">
                        <label for="automatik">Automatik</label>
                        <input class="form-check-input form-control" type="radio" id="automatik" name="transmission">
                    </div>
                </div>
                
            <div class="input-group">
                <div class="form-group my-3 mr-3">
                    <label for="model">Tip vozila</label>
                    <select name="type" class="form-select" aria-label="Izaberite" required>
                        <option value="sedan">Sedan</option>
                        <option value="kupe">Kupe</option>
                        <option value="kabriolet">Kabriolet</option>
                        <option value="karavan">Karavan</option>
                        <option value="suv">SUV</option>
                        <option value="kombi">Kombi</option>
                        <option value="limuzina">Limuzina</option>
                    </select>
                </div>
                <div class="form-group my-3 mx-3">
                    <label for="model">Gorivo</label>
                    <select id="gorivo" name="fuel" class="form-select" aria-label="Izaberite" required>
                        <option value="dizel">Dizel</option>
                        <option value="benzin">Benzin</option>
                        <option value="plin">Plin</option>
                        <option value="hibrid">Hibrid</option>
                        <option value="elektricni">Električni</option>
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
                <label for="images" class="mb-1">Slike vozila</label> <br>
                <input type="file" id="car-photo" name="images" accept="image/png, image/jpeg" required>
            </div>
            <div class="form-group">
              <label for="opis-kola">Opis vozila</label>
              <textarea name="descr" class="form-control" id="opis-kola" rows="5" required></textarea>
            </div>
        </form>
        <div class="form-group my-3">
            <button class="btn btn-dark" @click="submitData">Pošalji</button>
        </div>
    </div>
</template>
<script>
import $ from 'jquery';
import axios from 'axios';

export default {
    name: "CreateListing",
    mounted() {
        $('#customRange2').on('input', function(){
            let val = $('#customRange2').val()
        
            $('#rangeVal').val(val)
        });
        $('#rangeVal').on('input', function(){
            console.log('change')
            let val = $('#rangeVal').val()
            console.log(val)
            
            $('#customRange2').val(val)
        });
    },
    methods: {
        getCoordinates() {
            var addressValue = document.querySelector("#adresaVozila").value;
            var coordinates = null;
            axios({
                method: "get",
                url: `https://dev.virtualearth.net/REST/v1/Locations/${addressValue}?key=Al9hlQRWKffWXgWCo9DIxIenHGNvv7gkLztrBjFCJdInqHrVa2HXFyIdVoI8-DQ9`,
            }).then((response) => {
                var points = response.data.resourceSets[0].resources[0].point.coordinates;
                var dict = {"lat": points[0], "long": points[1]};
                console.log(dict)
                coordinates = JSON.stringify(dict);
            }).catch((err) => {
                console.log(err);
            });
            return coordinates;
        },
        submitData() {
            var formData = new FormData();
            var coordinates = this.getCoordinates();
            formData.append("coordinates", coordinates);
            formData.append("year", document.querySelector("#godinaProizvodnje"));
            var manafacturer = document.querySelector("#manafacturer");
            formData.append("manafacturer", manafacturer.options[manafacturer.selectedIndex].value);
            formData.append("model", document.querySelector("#model").value);
            var fuel = document.querySelector("#gorivo");
            formData.append("fuel", fuel[fuel.selectedIndex].value);
            formData.append("price_per_day", document.querySelector("#rangeVal").value);
            formData.append("manual", document.querySelector("#manual").value);
            formData.append("automatic", document.querySelector("#automatik").value);
            formData.append("descr", document.querySelector("#opis-kola").value);
            formData.append("images",  document.querySelector("#car-photo").files[0]);
            for (let key in formData.keys()) {
                console.log(key + " : "+ formData[key])
            }
        }
    }
}

</script>