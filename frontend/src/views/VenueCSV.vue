<template>
  <div>
    <adminNav />
    <div class="venue-details container mt-3">
      <h1 class="text-center mb-4">Venue Details</h1>
      <div v-if="venue" class="card container">
        <br>
        <h1 class="text-center">{{ venue.name }} </h1>
        <h4 class="text-center"> {{ venue.place }}, {{ venue.location }} | Capacity: {{ venue.capacity }} seats</h4>
        <h2 class="text-center"><a v-if="venue.screened.length > 0" :href="csvDownloadLink" class="btn btn-dark" :download="`${venue.name}_details.csv`">Download CSV</a></h2>
        <br/>
        <div v-if="venue.screened.length > 0" class="row">
          <div
            v-for="show in venue.screened"
            :key="show.show_id"
            class="col-lg-4 col-md-6 col-sm-12"
          >
            <div class="card show-details border p-3 mb-3">
              <h4>{{ show.show_name }}</h4>
              <p class="mb-2"><strong>Rating:</strong> {{ show.rating }}</p>
              <p class="mb-2"><strong>Price:</strong> {{ show.price }}</p>
              <p class="mb-2"><strong>Tags:</strong> {{ show.tags }}</p>
              <p class="mb-2"><strong>Day:</strong> {{ show.day }}</p>
              <p class="mb-2"><strong>Time:</strong> {{ show.time }}</p>
              <p class="mb-0"><strong>Booked Tickets:</strong> {{ show.booked }}</p>
            </div>
          </div>
        </div>
        <div v-else>
          <h5 class="text-center">No Shows being Screened in this Venue</h5>
        </div>
      </div>
      <div v-else>
        <h3>Loading Venue Details...</h3>
      </div>
    </div>
  </div>
</template>


  
  <script>
  import AdminNav from '../components/AdminNav'
  
  export default {
    components: {
      adminNav: AdminNav,
    },
    data() {
      return {
        venue: null,
        csvDownloadLink: '',
      };
    },
    created() {
      this.fetchVenueDetails();
    },
    methods: {
      async fetchVenueDetails() {
        try {
          const id = this.$route.params.id;
          const token = localStorage.getItem('access_token');
          const response = await fetch(`http://localhost:8000/api/admin/csv_download/${id}`, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          });
          const data = await response.json();
          this.venue = data;
          console.log(this.venue)
          this.generateCSV();
        } catch (error) {
          console.error(error);
        }
      },
      generateCSV() {
        if (this.venue !== null) {
          const csvContent = [
            ['Venue Name', 'Venue Location', 'Show Name', 'Rating', 'Price', 'Tags', 'Day', 'Time', 'Booked Tickets'],
            ...this.venue.screened.map(show => [
              this.venue.name,
              this.venue.location,
              show.show_name,
              show.rating,
              show.price,
              show.tags,
              show.day,
              show.time,
              show.booked,
            ]),
          ];
          const csvBlob = new Blob([csvContent.join('\n')], { type: 'text/csv' });
          this.csvDownloadLink = URL.createObjectURL(csvBlob);
        }
      },
    },
  };
  </script>
  
  <style>
  .venue-details {
    padding: 20px;
  }
  .show-details {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
  }
  </style>
  