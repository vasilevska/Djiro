<template>
    <div id="results" class="container pt-1 mt-2">
        <div class="row mt-2 pl-2">
            <div class="d-flex filteri mt-1">
                <h3>Sortiranje:&nbsp;&nbsp;</h3>
              <select name="sort" id="sortiranje" style="width:350px;" v-on:change="sortF($event)">
                <option value="bez-sort" selected>Izaberite sortiranje</option>
                <option value="god_desc">Godiste vozila (Od najvece do najmanje)</option>
                <option value="god_asc">Godiste vozila (Od najmanje do najvece)</option>
                <option value="km_desc">Kilometraza vozila (Od najvece do najmanje)</option>
                <option value="km_asc">Kilometraza vozila (Od najmanje do najvece)</option>
              </select>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <h3>Filteri:&nbsp;&nbsp;</h3>
              <button class="btn btn-primary form-control pl-5" style="width:200px;" @click="filters()">Filteri</button>
            </div>
        </div>
        <div class="d-flex filteri mt-1 d-none py-3" id="filteri">
            <hr>
            <input class="form-control me-2" type="text" placeholder="Godiste" style="width:200px;" id="godiste">
            <select name="markaS" id="markaS" style="width:200px;" class="mx-2">
                <option value="" selected>Izaberi Marku</option>
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
            <select name="tipS" id="tipS" style="width:230px;" class="mx-2">
                <option value="" selected>Izaberi tip Vozila</option>
                <option value="sedan">Sedan</option>
                <option value="kupe">Kupe</option>
                <option value="kabriolet">Kabriolet</option>
                <option value="karavan">Karavan</option>
                <option value="suv">SUV</option>
                <option value="kombi">Kombi</option>
                <option value="limuzina">Limuzina</option>
            </select>
            <select name="gorivoS" id="gorivoS" style="width:200px;" class="mx-2">
                <option value="" selected>Izaberi vrstu Gorivo</option>
                <option value="dizel">Dizel</option>
                <option value="benzin">Benzin</option>
                <option value="plin">Plin</option>
                <option value="hibrid">Hibrid</option>
                <option value="elektricni">Električni</option>
            </select>
            <button class="btn btn-primary mx-2" style="width:150px" @click="f2()">Filtriraj</button>
        </div>
        <hr>
        <div class="columns is-multiline">
            <div class="column is-8">
                <h2 class="is-size-2 has-text-centered">Cars</h2>
            </div>

            <div class="coulmn is-4" v-for="car in cars" v-bind:key="car.idc">
                <div class="box" style="padding: 10px;">
                    <div class="container">
                        <div class="row">
                            <div class="col-4">
                                <img v-bind:src="car.get_thumbnail">
                            </div>
                            <div class="col-4">
                                <h3 class="id-size-4">Model: {{car.model.name}}</h3>
                                <h3 class="id-size-4">Type: {{car.type}}</h3>
                                <!-- Fali ocena -->

                                <hr> 
                                <div class="row align-bottom">
                                    <div class="col-3"><button class="btn btn-primary" style="width:150px"><router-link v-bind:to="car.get_absolute_url" style="color: white;">
                                        Vise detalja</router-link></button></div>
                                    <div class="col-3 align-right">
                                        <h3 class="id-size-4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{car.price_per_day}}€/dan</h3>
                                    </div>
                                    
                                </div>

                            </div>
                        </div>
                    </div>
                    
                    
                </div>
            </div>

        </div>
    </div>
</template>

<style lang="scss">
    
</style>

<script>

import axios from 'axios'

export default {
    name: 'ListingView',
    data(){
        return{
            cars:[],
            cars_unselected_filters: []
        }
    },
    components:{

    },
    mounted(){
        this.getCarList()
    },
    methods:{
        getCarList(){
            axios
                .get('/api/list_of_all_cars/')
                .then(response =>{
                    this.cars = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },

        sortF: function(e){

            console.log(e.target.value)
            var tmp = e.target.value;

            switch (tmp){
                case "god_desc":
                    console.log(this.cars)
                    this.cars.sort(function(first, second) {
                        return second.year - first.year;
                    });
                    console.log(this.cars)
                break;
                case "god_asc":
                    this.cars.sort(function(first, second) {
                        return -(second.year - first.year);
                    });
                break;
                case "km_desc":
                    this.cars.sort(function(first, second) {
                        console.log(second.km)
                        console.log(first.km)
                        return second.km - first.km;
                    });
                break;
                case "km_asc":
                    this.cars.sort(function(first, second) {
                        return -(second.km - first.km);
                    });
                break;
                default:
                break;
            }

        },
        filters(){
            document.getElementById("filteri").classList.remove("d-none");
        },
        f2(){
            var e = document.getElementById("markaS");
            var marka = e.options[e.selectedIndex].value.toLowerCase();
            e = document.getElementById("tipS");
            var tip = e.options[e.selectedIndex].value.toLowerCase();
            e = document.getElementById("gorivoS");
            var gorivo = e.options[e.selectedIndex].value.toLowerCase();
            var godiste = document.getElementById("godiste").value;

            console.log(marka, tip, gorivo, godiste);

            var len = this.cars.length;

            var index_out = []

            for(var i = 0; i < len; i++){
                if(marka != '' && this.cars[i].model.manufacturer.name.toLowerCase() != marka){
                    this.cars_unselected_filters.push(this.cars[i]);
                    //this.cars.splice(i, 1);
                    index_out.push(i)
                    continue;
                }else if(tip != '' && this.cars[i].type.toLowerCase() != tip){
                    this.cars_unselected_filters.push(this.cars[i]);
                    //this.cars.splice(i, 1);
                    index_out.push(i)
                    continue;
                }else if(gorivo != '' && this.cars[i].fuel.toLowerCase() != gorivo){
                    this.cars_unselected_filters.push(this.cars[i]);
                    //this.cars.splice(i, 1);
                    index_out.push(i)
                    continue;
                }else if(godiste != '' && parseInt(this.cars[i].year) != godiste){
                    this.cars_unselected_filters.push(this.cars[i]);
                    //this.cars.splice(i, 1);
                    index_out.push(i)
                    continue;
                }

            }

            //izbacivanje iz liste auta
            for(i = index_out.length - 1; i >= 0; i--){
                this.cars.splice(index_out[i], 1);
            }

            len = this.cars_unselected_filters.length;

            //predstavlja koliko moramo filteri proci da bi se vratio u listing
            var indikator = 0;
            if(marka != ''){
                indikator += 1;
            }
            if(gorivo != ''){
                indikator += 1;
            }
            if(godiste != ''){
                indikator += 1;
            }
            if(tip != ''){
                indikator += 1;
            }
            index_out = []

            //ako su promenjena polja za filtriranje, pa mozda 
            for(i = 0; i < len; i++){
                var tmp = 0;
                if(marka != '' && this.cars_unselected_filters[i].model.manufacturer.name.toLowerCase() == marka){
                    tmp += 1;
                }
                if (tip != '' && this.cars_unselected_filters[i].type.toLowerCase() == tip){
                    tmp += 1;
                }
                if (gorivo != '' && this.cars_unselected_filters[i].fuel.toLowerCase() == gorivo){
                    tmp += 1;
                }
                if (godiste != '' && parseInt(this.cars_unselected_filters[i].year) == godiste){
                    tmp += 1;
                }
                if(tmp == indikator){
                    this.cars.push(this.cars_unselected_filters[i]);
                    index_out.push(i)
                }

            }

            //izbacivanje iz liste auta
            for(i = index_out.length - 1; i >= 0; i--){
                this.cars_unselected_filters.splice(index_out[i], 1);
            }

            document.getElementById("filteri").classList.add("d-none");
        }

    }
}
</script>

