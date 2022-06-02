<template>
    <div class="container">
        <div class="row">
            <div class="col-12" style="text-align: center;">
                <figure class="image mb-6">
                    <img v-bind:src="car.get_image" style="width: 70%; height: 70%;">
                </figure>
            </div>
        </div>
        <div class="row">
            <div class="col-6" style="text-align: center;">
                 <h3>{{car.year}}</h3>
                 <hr>
                 <div style="text-align: left;">
                    <h1>Opis:</h1>
                    <h4>{{car.descr}}</h4>
                 </div>
            </div>
            <div class="col-6">
                <h2>Cena: {{car.price_per_day}}€/dan</h2>
                <hr>
                <h3>Izaberite datume:</h3>
                <form style="margin: 10px;">
                    Od: <input type="date" name="datumOd" id="datumOd">
                    Do: <input type="date" name="datumDo" id="datumDo">
                    <div class="col-3" style="margin-top: 40px;"><button class="btn btn-primary" style="width:150px">
                        REZERVISI</button></div>
                </form>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios'

export default {
    name: 'CarDetails',
    data(){
        return{
            car:[]
        }
    },
    mounted(){
        this.getCar()
    },
    methods:{
        getCar(){
            const car_slug = this.$route.params.car_slug

            axios
                .get(`/api/car/${car_slug}`)
                .then(response =>{
                    this.car = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        }
    }
}
</script>