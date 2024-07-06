<template>
    <div>
        <userNav />
      <br />
      <h1 class="text-center">Upcoming Shows</h1>
      <br />
      <div class = 'user-home'>
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th></th>
            <th>Show</th>
            <th>Rating</th>
            <th>Screen</th>
            <th>Seats Available</th>
            <th>Day</th>
            <th>Time</th>
            <th>Location</th>
            <th>Book Now!</th>
          </tr>
        </thead>
        <tbody class="table-dark">
            <tr v-for="item in upcomingShows" :key="item.screening.id">
          <td><img :src="item.screening.show.img" class="table-image" /></td>
          <td>{{ item.screening.show.name }}</td>
          <td>{{ item.screening.show.rating }}</td>
          <td>{{ item.screening.venue.name }}</td>
          <td>{{ calculateSeatsAvailable(item.screening.venue.capacity, item.num_results) }}</td>
          <td>{{ formatDate(item.screening.day) }}</td>
          <td>{{ formatTime(item.screening.time) }}</td>
          <td>{{ item.screening.venue.location }}, {{ item.screening.venue.place }}</td>
          <td v-if="calculateSeatsAvailable(item.screening.venue.capacity, item.num_results) > 0">
            <router-link :to="{ name: 'Booking', params: { id: item.screening.id } }" class="btn btn-dark">
                Buy Ticket
            </router-link>
          </td>
          <td v-else>
            <button class="btn btn-secondary" disabled>SOLD OUT</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    </div>
  </template>
  
  <script>
  import UserNav from "../components/UserNav";
  export default {
    components: {
        userNav : UserNav,
    },
    data() {
    return {
      packed: [],
      screenings: [],
      upcomingShows: [],
      access_token: localStorage.getItem("access_token"),
    };
  },
  async mounted() {
    await this.fetchUserHomeData();
    this.filterUpcomingShows();
  },
  methods: {
    async fetchUserHomeData() {
      try {
        const response = await fetch("http://localhost:8000/api/user/home", {
          headers: {
            Authorization: `Bearer ${this.access_token}`,
          },
        });
        const data = await response.json();
        this.packed = data.packed;
        this.screenings = data.screenings;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    filterUpcomingShows() {
  this.upcomingShows = this.packed
    .map(packedItem => {
      const screening = this.screenings.find(screeningItem => screeningItem.id === packedItem.screening.id);
      if (screening) {
        return { screening, num_results: packedItem.num_results };
      }
    })
    .filter(Boolean);
},
    calculateSeatsAvailable(capacity, numResults) {
      const seatsAvailable = capacity - numResults;
      return seatsAvailable > 0 ? seatsAvailable : 0;
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    },
    formatTime(timeStr) {
      const time = new Date(`1970-01-01T${timeStr}`);
      return time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    },
  },
  };
  </script>
  
  <style scoped>
.user-home {
  margin: 0 auto;
  padding: 20px;
}

.table-image {
  max-width: 100px;
  border-radius: 10px;
}

.table{
    background-color:bisque !important;
}
</style>
  