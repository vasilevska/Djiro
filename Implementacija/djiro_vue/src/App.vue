<template>
  <div>
    <div class="header">
      <!-- <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> -->
      <navigation-bar></navigation-bar>
    </div>

    <div class="container">
      <router-view/>
    </div>

    <div class="footer"></div>
  </div>
</template>

<style>
@import "../node_modules/bootstrap";
</style>

<script>
import NavigationBar from "./components/NavigationBar.vue";

export default {
  name: "App",
  components: {
    NavigationBar,
  },
};
</script>
