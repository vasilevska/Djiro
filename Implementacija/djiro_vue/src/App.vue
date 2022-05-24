<template>
  <div>
    <div class="header">
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </nav>
    </div>

    <div class="container">
      <router-view />
    </div>

    <div class="footer"></div>
  </div>
</template>

<style>
@import "../node_modules/bootstrap";
</style>
