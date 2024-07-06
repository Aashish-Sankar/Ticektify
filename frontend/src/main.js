import { createApp } from 'vue'
import App from './App'
import router from './router'
import store from './store'
import VueApexCharts from "vue3-apexcharts";
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
app.use(router);
app.use(store);
app.use(VueApexCharts);
app.mount('#app');