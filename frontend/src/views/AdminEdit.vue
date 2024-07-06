<template>
  <div class = "form-container">
    <section class='form'>
      <br/>
      <h2 style="text-align: center;">&nbsp;&nbsp;EDIT SCREENING&nbsp;&nbsp;</h2>
      <form @submit.prevent="editScreening">
        <br/>
        <div>
          <label>Movie: </label>
          <select v-model = "selectedShow" required>
            <option v-for="show in shows" :key="show.id" :value="show">{{ show.name }}</option>
          </select>
        </div>
        <div>
          <label><br>Venue: </label>
          <select v-model = "selectedVenue" required>
            <option v-for="venue in venues" :key="venue.id" :value="venue">{{ venue.name }}</option>
          </select>
        </div>
        <div>
          <label>Date:</label>
          <input type="date" v-model="selectedDate" min="2021-01-01" max="2023-12-31" required>
        </div>
        <div>
          <label>Time:</label>
          <input type="time" v-model="selectedTime" required>
        </div>
        <br/>
        <div>
          <input class='submit' type="submit" value="Edit"/>
        </div>
      </form>
    </section>
  </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        shows:[],
        venues:[],
        selectedShow: null, 
        selectedVenue: null, 
        selectedDate: '',  
        selectedTime: '',  
        access_token: localStorage.getItem('access_token'),
      };
    },
    created() {
        this.fetchdata();
    },
    methods: {
        fetchdata() {
      const id = this.$route.params.id;

      fetch(`http://localhost:8000/api/admin/edit/${id}`, {
        headers: {
          Authorization: `Bearer ${this.access_token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
            this.venues = data.venues;
            this.shows = data.shows;
            this.selectedShow = this.shows.find((show) => show.id === data.current_data.show.id);
          this.selectedVenue = this.venues.find((venue) => venue.id === data.current_data.venue.id);
          this.selectedDate = data.current_data.day;
          this.selectedTime = data.current_data.time;
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    },
      editScreening() {
        const formData = {
          Shows: this.selectedShow.id,
          venue: this.selectedVenue.id,
          day: this.selectedDate,
          time: this.selectedTime,
        };
        const id = this.$route.params.id;
        console.log(id);
        fetch(`http://localhost:8000/api/admin/edit/${id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.access_token}`,
          },
          body: JSON.stringify(formData),
        })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.$router.push('/admin/home');
        })
        .catch((error) => {
          console.error('Error editing screening:', error);
        });
      },
    },
  };
  </script>
  