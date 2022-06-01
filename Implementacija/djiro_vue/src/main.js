import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
var cors = require('cors');
createApp(App).use(store).use(router).use(cors).mount("#app");
