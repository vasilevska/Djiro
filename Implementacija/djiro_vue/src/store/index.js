import { getAPI } from "@/axios-api";
import { createStore } from "vuex";

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    id: "",
    APIData: "",
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  mutations: {
    updateStorage(state, { access, refresh, id }) {
      state.accessToken = access;
      state.refreshToken = refresh;
      state.id = id;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", access);
      localStorage.setItem("id", id);
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.id = null;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("id");
    },
  },
  actions: {
    userLogout(context) {
      if (context.getters.loggedIn) {
        context.commit("destroyToken");
      }
    },
    userLogin(context, userCredentials) {
      return new Promise((resolve, reject) => {
        getAPI
          .post("/api/api-token/", {
            email: userCredentials.email,
            password: userCredentials.password,
          })
          .then((response) => {
            var access = response.data.access;
            var refresh = response.data.refresh;
            getAPI
              .get("/api/get-id/", {
                headers: { Authorization: `Bearer ${access}` },
              })
              .then((response) => {
                // TODO: Obrisi odmah posle testiranja
                console.log(response.data.id);
                context.commit("updateStorage", {
                  access: access,
                  refresh: refresh,
                  id: response.data.id,
                });
              })
              .catch((err) => {
                console.log(err);
                reject();
              });
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject();
          });
      });
    },
    fetchAccessToken({ commit }) {
      commit("updateStorage", {
        access: localStorage.getItem("access"),
        refresh: localStorage.getItem("refresh"),
        id: localStorage.getItem("id"),
      });
    },
  },
  modules: {},
});
