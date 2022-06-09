<template>
     <div class="container" v-if="!sending">
       <form enctype="multipart/form-data" id="my-form">
        <p class="h3 my-5">Unesite infromacije o kolima</p>
            <div class="form-group my-3">
                <label for="adresaVozila">Gde se Vaše vozilo nalazi?</label>
                <input type="text" class="form-control" name="address" id="adresaVozila" placeholder="Unesite adresu" required>
            </div>
            <div class="input-group">                
                <div class="form-group my-3 mr-3">
                    <label for="godinaProizvodnje">Godina proizvodnje</label>
                    <input type="number" min="1900" max = "2099" step="1" value="2022" class="form-control" name="godinaProizvodnje" id="godinaProizvodnje" required>
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
                    <label for="km">Kilometraža</label>
                    <input type="number" min="0" max = "1000000" step="1"  class="form-control" name="km" id="km" required>
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
                    <label for="type">Tip vozila</label>
                    <select name="type" id="type" class="form-select" aria-label="Izaberite" required>
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
                    <label for="fuel">Gorivo</label>
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
                        <label for="customRange2">Cena po danu (u &euro;): </label> <input type="number" min="10" max = "205" class="form-control mx-3" size="3" id="rangeVal">
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
    <div class="container" v-else>
        <div class="row align-items-center justify-items-center">
            <div class="col-auto">
                <ring-loader :color="color1" :height="height"></ring-loader>
            </div>
        </div>
        
    </div>
</template>
<script>
import $ from 'jquery';
import axios from 'axios';
import RingLoader from 'vue-spinner/src/RingLoader.vue'

export default {
    name: "CreateListing",
    data() {
        return {
        infos: null,
        errors: null,
        sending: false,
        color1: '#3AB982',
        height: '50px'
        };
    },
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
            return axios({
                method: "get",
                url: `https://dev.virtualearth.net/REST/v1/Locations/${addressValue}?key=Al9hlQRWKffWXgWCo9DIxIenHGNvv7gkLztrBjFCJdInqHrVa2HXFyIdVoI8-DQ9`,
            });
        },
        getData() {
            var formData = new FormData();  
            let yr = document.querySelector("#godinaProizvodnje").value;
            formData.append("year", yr);
            var manafacturer = document.querySelector("#manafacturer");
            formData.append("manufacturer", manafacturer.options[manafacturer.selectedIndex].value);
            formData.append("car_model", document.querySelector("#model").value);
            var fuel = document.querySelector("#gorivo");
            formData.append("fuel", fuel[fuel.selectedIndex].value);
            formData.append("price_per_day", document.querySelector("#rangeVal").value);
            let manual = document.querySelector("#manual").value;
            if(manual){
                formData.append("transmision", "manual");
            }else{
                formData.append("transmision", "automatic")
            }
            var type = document.querySelector("#type")
            formData.append("type", type[type.selectedIndex].value);
            formData.append("descr", document.querySelector("#opis-kola").value);
            formData.append("images",  document.querySelector("#car-photo").files[0]);
            formData.append("km", parseInt(document.getElementById("km").value));
            return formData;
        },
        dispalyInfo(info){
            this.infos=[];
            for (let key in info) {
                    this.infos.push(key + " : " + info[key]);
                }
        },
        resetInfo(){
            this.infos = null;
        },
        resetErrors(){
            this.errors = null;
        },
        displayError(err){
            this.errors = [];
            for (let key in err) {
                    this.errors.push(key + " : " + err[key]);
                    console.log(err[key]);
                }
        },
        sendForm(formData){
            axios({
                method: "post",
                url: "http://127.0.0.1:8000/api/create_car/",
                data: formData,
                headers: { 
                "Content-Type": "multipart/form-data" ,
                "Authorization" : `Bearer ${this.$store.state.accessToken}`
                },
            })
                .then((response) => {
                this.dispalyInfo(response.data);
                this.sending=false;
                this.$router.push({name : "home"});
                })
                .catch((err) => {
                this.displayError(err.response.data);
                this.displayError(err.message);
                this.sending = false;
                });
        },
        submitData(){
            this.resetInfo();
            this.resetErrors();
            this.sending = true;
            let self = this;
            var formData = this.getData();
            this.getCoordinates()
            .then((response) => {
                var points = response.data.resourceSets[0].resources[0].point.coordinates;
                var dict = {"lat": points[0], "long": points[1]};
                console.log(dict)
                formData.append("coordinates", JSON.stringify(dict));
                self.sendForm(formData);

            }).catch((err) => {
                this.displayError(err)
            });      
        }
    },
    components:{
        RingLoader
    }
}

</script>