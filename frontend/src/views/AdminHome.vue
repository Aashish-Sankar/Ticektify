<template>
    <div >
      <adminNav />
      <br />
      <h1 style="text-align: center;">SCREENINGS</h1>
      <br />
      <div>
        <div v-if="screenings.length > 0" class="container py-0 px-0">
          <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-5 ">
          <div v-for="(item, index) in packed" :key="index" class="col">
            <div class="card h-100">
              <div class="card-body">
                <p>Name: {{ item.screening?.show?.name }}</p>
                <p>Venue: {{ item.screening?.venue?.name }}</p>
                <p>Total Seats: {{ item.screening?.venue?.capacity }}</p>
                <p>Seats Available: {{ item.seats_available }}</p>
                <p>Seats Booked: {{ item.result }}</p>
                <p>Show Date: {{ formatDate(item.screening?.day) }}</p>
                <p>Show Time: {{ item.screening?.time }}</p>
                <p>Location: {{ item.screening?.venue?.place }}, {{ item.screening?.venue?.location }}</p>
                <p v-if="item.result > 0">
                  Cannot modify screening<br />
                  with bookings
                </p>
                <p v-else>
                  <a @click="deleteScreening(item.screening?.id)"  href="#">Delete</a>
                  |
                  <router-link class="link-style " :to="{name: 'adminEdit',params:{id:item.screening?.id}}">Edit</router-link>
                </p>
              </div>
            </div>
            <br />

          </div>
        
          <div class="card splcard">
              <a class="button" :href="'/admin/add'">
                <img src="https://cdn-icons-png.flaticon.com/512/8191/8191584.png" width="50" height="50" />
              </a>
            </div>
            </div>
        </div>
        <div v-else>
          <p style="text-align: center">THERE ARE NO SCHEDULED SCREENINGS</p>
          <p style="text-align: center">
            <a class="button card-btn" :href="'/admin/add'">Add new Screening</a>
          </p>
        </div>
      </div>
      <br />
    </div>
  </template>
  
  <script>
  import AdminNav from "../components/AdminNav"
  export default {
  components: {
    adminNav: AdminNav,
  },
  name: "AdminHome",
  data() {
    return {
      screenings: [],
      access_token: localStorage.getItem('access_token'),
    };
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString("en-GB");
    },
    async fetchData() {
      console.log("Access Token:", this.access_token); 
      try {
        const response = await fetch("http://127.0.0.1:8000/api/admin/home",
          {
            headers: {
              "Authorization": `Bearer ${this.access_token}`,
            },
          },
        );
        const data = await response.json();
        this.screenings = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    deleteScreening(id) {
      if (confirm("Are you sure you want to delete this item?")) {
        fetch(`http://127.0.0.1:8000/api/admin/delete/${id}`, {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${this.access_token}`,
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Error deleting screening");
            }
           
            this.screenings = this.screenings.filter((item) => item.screening?.id !== id);
            alert("Screening deleted successfully");
          })
          .catch((error) => {
            console.error("Error deleting screening:", error);
            alert("Error deleting screening");
          });
      }
    },
  },
  computed: {
    packed() {
      return this.screenings.map((item) => ({
        screening: item.screening,
        result: item.num_results,
        seats_available: item.screening?.venue?.capacity - item.num_results,
      }));
    },
  },
  mounted() {
    this.fetchData();
  },
  beforeRouteEnter(to, from, next) {
    if (!to.meta.requiresAuth || !to.meta.requiresAdmin) {
      next();
    } else if (localStorage.getItem("access_token") === null) {
      next({
        path: "/admin/login",
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  },
};
  </script>
  
  <style>
  @import '../assets/styling.css'
  </style>