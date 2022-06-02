<template>
    <div id="results" class="container pt-1 mt-2">
        <div class="row mt-2 pl-2">
            <div class="d-flex filteri mt-1">
                <h3>Sortiranje:&nbsp;&nbsp;</h3>
              <select name="sort" id="sortiranje" class="form-control" style="width:280px;" v-model="selected" v-on:change="sortF($event)">
                <option value="bez-sort">Izaberite sortiranje</option>
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
              <button class="btn btn-primary form-control pl-5" style="width:200px;">Filteri</button>
            </div>
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
                                        <h3 class="id-size-4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{car.price_per_day}}$/dan</h3>
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
            cars:[]
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

        }

    }
}
</script>

