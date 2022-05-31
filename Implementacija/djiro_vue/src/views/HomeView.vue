<template>
  <div class="home">
    This is home
  <car-card :carInfo="null"></car-card>
  </div>
</template>

<script>
import CarCard from '../components/CarCard.vue';

export default {
  name: "HomeView",
  components: { CarCard },
};
</script>
