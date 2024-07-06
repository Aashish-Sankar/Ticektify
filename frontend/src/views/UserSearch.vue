<template>
    <div>
    <userNav/>
    <div class="user-home">
      <br />
      <h1 class="text-center">Search Results</h1>
      <br />
  
      <table class="table-bordered table">
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
            <th></th>
          </tr>
        </thead>
        <tbody class="table-dark">
          <tr v-for="screening in searchResults" :key="screening.id">
            <td><img :src="screening.show.img" width="120" style="border-radius: 15px;" class="table-image" /></td>
            <td>{{ screening.show.name }}</td>
            <td>{{ screening.show.rating }}</td>
            <td>{{ screening.venue.name }}</td>
            <td>{{ calculateSeatsAvailable(screening) }}</td>
            <td>{{ formatDate(screening.day) }}</td>
            <td>{{ formatTime(screening.time) }}</td>
            <td>{{ screening.venue.location }}, {{ screening.venue.place }}</td>
            <td v-if="calculateSeatsAvailable(screening) > 0">
              <a :href="'user/booking/' + screening.id" class="btn btn-dark">Buy Ticket</a>
            </td>
            <td v-else>SOLD OUT</td>
          </tr>
        </tbody>
      </table>
    </div>
</div>
  </template>
  
  <script>
  import userNav from '../components/UserNav'
  import { mapState } from 'vuex';
  export default {
    name: 'userSearch',
    components:{
        userNav,
    },
    computed: {
    ...mapState(['searchResults']),
},
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
      },
      formatTime(timeString) {
        const time = new Date(`1970-01-01T${timeString}`);
        return time.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
      },
      calculateSeatsAvailable(screening) {
      if (screening.bookings && screening.bookings.length > 0) {
        const bookedSeats = screening.bookings.reduce((totalSeats, booking) => totalSeats + booking.seats, 0);
        const seatsAvailable = screening.venue.capacity - bookedSeats;
        return seatsAvailable;
      } else {
        return screening.venue.capacity;
      }
    },
    },
  };
  </script>

<style>
.user-home {
  margin: 0 auto;
  padding: 20px;
}

.table-image {
  max-width: 100px;
  border-radius: 10px;
}
</style>
  