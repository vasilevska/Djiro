<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-6">
        <h1>Sign In</h1>
        <form id="login-form" action="profil.html">
          <input
            type="text"
            name="username"
            class="username form-control my-3"
            placeholder="Username"
            v-model="username"
          />
          <input
            type="password"
            name="password"
            class="password form-control"
            placeholder="Password"
            v-model="password"
          />
          <p class="error">
            {{ error }}
          </p>
          <p>
            New User?&nbsp;<router-link to="/registration"
              >Create account</router-link
            >
          </p>
          <input
            class="btn btn btn-outline-secondary"
            type="button"
            value="Login"
            @click="submitInfo"
          />
        </form>
      </div>
    </div>
  </div>
</template>
<style>
h1 {
    padding: 10px;
}
p {
    padding-left: 6px;
    padding-top: 2px
}
.error {
    color: red;
}
</style>
<script>
export default {
  name: "LoginView",
  data() {
      return {
          username: "",
          pasword: "",
          error: ""
      }
  },
  setup() {},
  methods: {
      submitInfo() {
          if (this.username == "" || this.pasword == "") {
              this.error = "Please fill both username and password fields."
          }
      }
  }
};
</script>
