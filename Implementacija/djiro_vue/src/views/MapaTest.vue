<template>    
    <template v-if="ucitava">
        <h1>Ucitava se</h1>
      </template>

      <template v-else>
        <MapComponent :coords="coords" :center="center"></MapComponent>
      </template>
</template>   

<script>
    import axios from 'axios'
    import MapComponent from '../components/Map/Map.vue';
    export default{
        name: 'MapaTest',
    data(){
        return{
            ucitava: true,
            coords: null,
            center: null,
        }
    },
    methods:{
        getCoords(){
            let self = this;
                axios.get('http://127.0.0.1:8000/mapa/')
                .then(response =>{
                    var data = JSON.parse(response.data);
                    console.log(data);
                    self.coords = data['coords'];
                    self.center = data['center'];
                    self.ucitava = false
                })
                .catch(error =>{
                    console.log(error)
                })  
            
               
        }
    },
    created(){
        this.getCoords();
    },
    components:{
        MapComponent
        }
    }
</script>