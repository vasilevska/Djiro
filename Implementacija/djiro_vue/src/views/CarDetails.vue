<template>
    
    <div class="page-car">
        <div class="columns is-multiline">
            <div class="column is-9">
                <figure class="image mb-6">
                    <img v-bind:src="car.get_image">
                </figure>
                
                <h1>{{car.descr}}</h1>

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
            car:{}
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