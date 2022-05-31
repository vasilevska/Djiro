import { getAPI } from "@/axios-api";
import { createStore } from "vuex";

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    APIData: "",
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  mutations: {
    updateStorage(state, { access, refresh }) {
      state.accessToken = access;
      state.refreshToken = refresh;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", access);
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
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
            context.commit("updateStorage", {
              access: response.data.access,
              refresh: response.data.refresh,
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
      });
    },
  },
  modules: {},
});
