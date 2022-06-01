<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <router-link to="/" class="navbar-brand"
        ><strong>Điro</strong></router-link
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
          <li class="nav-item" v-if="accessToken == null">
            <router-link to="/registration" class="nav-link"
              >Register</router-link
            >
          </li>
          <!-- add v-if when you want to show an elemetn only if condition is satisified -->
          <li class="nav-item" v-if="accessToken == null">
            <router-link to="/login" class="nav-link">Sign In</router-link>
          </li>
          <li class="nav-item" v-if="accessToken != null">
            <router-link to="/" class="nav-link">Become a Djiler</router-link>
            <!-- Change path when car form is made -->
          </li>
          <li class="nav-item dropdown" v-if="accessToken != null">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDarkDropdownMenuLink"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              User
            </a>
            <ul
              class="dropdown-menu dropdown-menu-dark"
              aria-labelledby="navbarDarkDropdownMenuLink"
            >
              <li>
                <router-link class="dropdown-item" to="/profile"
                  >Profile</router-link
                >
              </li>
              <li>
                <router-link class="dropdown-item" to="/verification"
                  >Verify driving license</router-link
                >
              </li>
              <!-- Change path when profile view is made-->
              <li>
                <router-link class="dropdown-item" to="/logout"
                  >Logout</router-link
                >
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "NavigationBar",
  computed: mapState(["accessToken", "id"]),
  setup() {},
};
</script>
