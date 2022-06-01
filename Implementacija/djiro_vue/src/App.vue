<template>
  <div>
    <div class="header">
      <navigation-bar></navigation-bar>
    </div>

    <div class="container-fluid p-0">
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
