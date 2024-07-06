<template>
    <div class="user-home">
      <table class="table-bordered table table-dark">
        <thead>
          <tr>
            <th></th>
            <th>Title</th>
            <th>Screen</th>
            <th>Seats Reserved</th>
            <th>Day</th>
            <th>Time</th>
            <th>Booked Day</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>
              <img :src="booking.screening.show.img" width="100" style="border-radius: 15px;" class = "table-image"/>
            </td>
            <td>{{ booking.screening.show.name }}</td>
            <td>{{ booking.screening.venue.name }}</td>
            <td>{{ booking.seats }}</td>
            <td>{{ formatDate(booking.screening.day) }}</td>
            <td>{{ formatTime(booking.screening.time) }}</td>
            <td>{{ booking.date_time }}</td>
            
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      bookings: Array,
    },
    methods: {
      formatDate(date) {
        return new Date(date).toLocaleDateString();
      },
      formatTime(time) {
        return new Date(`1970-01-01T${time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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

</style>
  