<template>
  <div class="about">
    <h1>This is an about page</h1>
    <Reservations />
  </div>
</template>

<script>
  import Reservations from "../components/ReservationsDriver.vue";
  export default{
    name: "AboutView",
    components: {
      Reservations,
    }
  }
</script>

