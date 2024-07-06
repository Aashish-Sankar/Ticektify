<template>
  <div class="form-container">
    <section class="form">
      <br />
      <h2 style="text-align: center">&nbsp;&nbsp;ADD A NEW SCREENING&nbsp;&nbsp;</h2>
      <br />

      <form v-if="shows.length > 0 && venues.length > 0" @submit.prevent="addScreening">
        <div>
          <label>Show:</label>
          <select v-model="selectedShow" required>
            <option v-for="show in shows" :key="show.id" :value="show.id">{{ show.name }}</option>
          </select>
        </div>
        <div>
          <label>Venue:</label>
          <select v-model="selectedVenue" required>
            <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{ venue.name }}</option>
          </select>
        </div>
        <div>
          <label>Date:</label>
          <input type="date" v-model="selectedDate" :min="minDate" :max="maxDate" required />
        </div>
        <div>
          <label>Time:</label>
          <input type="time" v-model="selectedTime" required />
        </div>
        <br />
        <div>
          <input class="submit" type="submit" value="Add" />
        </div>
      </form>
      <div v-else>
        Loading...
      </div>
    </section>
  </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        shows: [],
        venues: [],
        selectedShow: '',
        selectedVenue: '',
        selectedDate: '',
        selectedTime: '',
        minDate: '2021-01-01',
        maxDate: '2023-12-31',
        access_token: localStorage.getItem("access_token"),
      };
    },
    mounted() {
      this.getData();
    },
    methods: {
      async getData() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/admin/add', {
          headers: {
            Authorization: `Bearer ${this.access_token}`,
          },
        });
          const data = await response.json();
          this.shows = data.Shows;
          this.venues = data.venues;
          this.selectedDate = data.current_day;
        } catch (error) {
          console.error(error);
        }
      },
      async addScreening() {
        const newScreening = {
          Shows: this.selectedShow,
          venue: this.selectedVenue,
          day: this.selectedDate,
          time: this.selectedTime,
        };
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/admin/add', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${this.access_token}`,
            },
            body: JSON.stringify(newScreening),
          });

          this.$router.push('/admin/home');
          const data = await response.json();
          console.log(response)
          console.log(data)
          this.$router.push('/admin/home');
          alert(data.message);
          
        } catch (error) {
          console.error(error);
        }
      },
    },
  };
  </script>
  