<template>
    <section>
        <adminNav/>
      <br />
      <h1 style="text-align: center;">VENUES</h1>
      <br />
      <div class="container py-1 px-2">
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 ">
        <div v-for="venue in venues" :key="venue.id" class="col">
          <div class="card h-100">
            <div class="card-body">
              <p>Name: {{ venue.name }}</p>
              <p>Capacity: {{ venue.capacity }}</p>
              <p>Location: {{ venue.place }}</p>
              <p>City: {{ venue.location }}</p>
              <p>
                <a
                  href="#"
                  @click="deleteVenue(venue.id)"
                  >Delete</a
                > |
                <router-link :to="{ name: 'editVenue', params: { id: venue.id }}">Edit</router-link>
                |
                <router-link :to="{ name: 'venueCSV', params: { id: venue.id }}">More</router-link>
              </p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 splcard">
            <router-link :to="{ name: 'venueAdd' }" class="button" style="display:block;">
              <img src="https://cdn-icons-png.flaticon.com/512/8191/8191584.png" width="50" height="50">
            </router-link>
          </div>
        </div>
      </div>
    </div>
    </section>
  </template>
  
<script>
import AdminNav from "../components/AdminNav";
export default {
  components: {
    adminNav: AdminNav,
  },
  data() {
    return {
      venues: [],
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      fetch("http://localhost:8000/api/admin/venues", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.venues = data;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    deleteVenue(id) {
      if (confirm("Are you sure you want to delete this item?")) {
        fetch(`http://localhost:8000/api/admin/venue_delete/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            this.fetchData();
          })
          .catch((error) => {
            console.error("Error deleting venue:", error);
          });
      }
    },
  },
};
</script>