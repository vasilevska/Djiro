<template>
  <div class="container">
    <div class="main-body">
      <div class="row gutters-sm">
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <img
                  alt="Profile picture"
                  class="rounded-circle"
                  width="150"
                  v-bind:src="user.get_thumbnail"
                />
                <div class="mt-3 text-center">
                  <h4>{{ user.first_name + " " + user.last_name }}</h4>
                  <p
                    class="text-secondary mb-1"
                    v-if="$store.state.user['is_djiler']"
                  >
                    Điler
                  </p>
                  <p v-if="rating != null">
                    {{ rating }} <font-awesome-icon icon="star" />
                  </p>
                  <p v-if="rating == null">ovaj korisnik nema ocene</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <div class="card mb-3">
            <div class="card-body">
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Ime</h6>
                </div>
                <div class="col-sm-9 text-secondary">{{ user.first_name }}</div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Prezime</h6>
                </div>
                <div class="col-sm-9 text-secondary">{{ user.last_name }}</div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Email</h6>
                </div>
                <div class="col-sm-9 text-secondary">{{ user.email }}</div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">Telefon</h6>
                </div>
                <div class="col-sm-9 text-secondary">{{ user.tel }}</div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <h6 class="mb-0">O meni</h6>
                </div>
                <div class="col-sm-9 text-secondary">
                  {{ user.bio }}
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-12">
                  <router-link
                    class="btn btn-dark"
                    :to="'/edit-profile/' + this.$store.state.id"
                    v-if="myProfile == true"
                    >Edit</router-link
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<!-- "https://www.bootdey.com/snippets/view/profile-edit-data-and-skills" -->
<style scoped>
body {
  margin-top: 20px;
  color: #1a202c;
  text-align: left;
  background-color: #e2e8f0;
}
.main-body {
  padding: 15px;
}
.card {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm > .col,
.gutters-sm > [class*="col-"] {
  padding-right: 8px;
  padding-left: 8px;
}
.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}
.h-100 {
  height: 100% !important;
}
.shadow-none {
  box-shadow: none !important;
}
</style>
<script>
import axios from "axios";

export default {
  name: "ProfileView",
  data() {
    return {
      user: null,
      myProfile: false,
      rating: null,
    };
  },
  watch: { 
    $route(to, from) { 
      // React to route changes... 
      if (to !== from) { 
        location.reload(); 
        } 
    } 
  },
  created() {
    // Check if you can edit user profile
    if (this.$route.params.id == this.$store.state.id) {
      this.myProfile = true;
    }
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/api/get-user/?id=${this.$route.params.id}`,
    })
      .then((response) => {
        // Get the first and only user from the response
        this.user = response.data.results[0];
      })
      .catch((err) => {
        console.log(err);
      });
    if (this.$store.state.user["is_djiler"]) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/rating/djiler/${this.$route.params.id}`,
      })
        .then((response) => {
          // Get the first and only user from the response
          this.rating = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/rating/driver/${this.$route.params.id}`,
      })
        .then((response) => {
          // Get the first and only user from the response
          this.rating = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
};
</script>
