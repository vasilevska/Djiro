<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">
        <img src="@/assets/djiro_logo.png" alt="logo" style="height: 40px" />
        <strong> Điro</strong></router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarToggler"
        aria-controls="navbarToggler"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarToggler">
        <ul class="navbar-nav ms-auto">
          <li
            class="nav-item"
            v-if="accessToken == null || accessToken == 'null'"
          >
            <router-link to="/registration" class="nav-link"
              >Registruj se</router-link
            >
          </li>
          <!-- add v-if when you want to show an elemetn only if condition is satisified; needs to account for 'null' string value -->
          <li
            class="nav-item"
            v-if="accessToken == null || accessToken == 'null'"
          >
            <router-link to="/login" class="nav-link">Sign In</router-link>
          </li>
          <li
            class="nav-item"
            v-if="accessToken != null && accessToken != 'null'"
          >
            <router-link to="/create-listing" class="nav-link"
              >Postani Điler</router-link
            >
            <!-- TODO: Change path when car form is made -->
          </li>
          <li
            class="nav-item dropdown"
            v-if="accessToken != null && accessToken != 'null'"
          >
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDarkDropdownMenuLink"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Korisnik
            </a>
            <ul
              class="dropdown-menu dropdown-menu-dark"
              aria-labelledby="navbarDarkDropdownMenuLink"
            >
              <li>
                <router-link
                  class="dropdown-item"
                  :to="'/profile/' + this.$store.state.id"
                  >Profil</router-link
                >
              </li>
              <li>
                <router-link class="dropdown-item" to="/reservations"
                  >Moje rezervacije</router-link
                >
              </li>
              <li>
                <router-link class="dropdown-item" to="/verification"
                  >Verifikuj vozačku</router-link
                >
              </li>
              <li>
                <router-link class="dropdown-item" to="/logout"
                  >Izloguj se</router-link
                >
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<style scoped>
.navbar {
  padding-right: 50px;
}
.dropdown-menu-dark {
  z-index: 10000;
}
</style>
<script>
import { mapState } from "vuex";
export default {
  name: "NavigationBar",
  computed: mapState(["accessToken", "id"]),
  setup() {},
};
</script>
