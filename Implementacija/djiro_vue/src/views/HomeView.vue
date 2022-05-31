<template>
  <div class="home">
    This is home
  <!-- <car-card :carInfo="null"></car-card> -->
  </div>
</template>

<script>
// import CarCard from '../components/CarCard.vue';
import { getAPI } from '@/axios-api';
import { mapState } from 'vuex';

export default {
  name: "HomeView",
  components: { },
  computed: mapState(['APIData']),
  created() {
    // TODO: Change this with car api and car cards, this only served for testing
    getAPI.get('/api/sample', {headers : {Authorization: `Bearer ${this.$store.state.accessToken}`}})
    .then(response => {
      this.$store.state.APIData = response.data
    })
      .catch(err => {
        console.log(err);
      })
  }
};
</script>
