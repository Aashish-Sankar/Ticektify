<template>
    <div class="form-container">
    <section class="form">
      <br />
      <h2 style="text-align: center;">Add Venue</h2>
      <form @submit.prevent="addVenue">
        <br />
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" v-model="name" class="form-control" id="name" placeholder="Venue Name" required />
        </div>
        <br />
        <div class="form-group">
          <label for="capacity">Capacity</label>
          <input type="text" v-model="capacity" class="form-control" id="capacity" placeholder="Enter capacity" required />
        </div>
        <br />
        <div class="form-group">
          <label for="place">Location</label>
          <input type="text" v-model="location" class="form-control" id="place" placeholder="Enter location" required />
        </div>
        <br />
        <div class="form-group">
          <label for="location">City</label>
          <input type="text" v-model="place" class="form-control" id="location" placeholder="Enter City" required />
        </div>
        <br />
        <button type="submit" class="btn btn-primary">Add</button>
      </form>
    </section>
</div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        name: '',
        capacity: '',
        location: '',
        place: '',
        access_token: localStorage.getItem("access_token"),
      };
    },
    methods: {
      addVenue() {
        const newVenue = {
          name: this.name,
          capacity: this.capacity,
          location: this.place,
          place: this.location,
        };
  
        fetch('http://localhost:8000/api/admin/venue_add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.access_token}`,
        },
        body: JSON.stringify(newVenue),
      })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message);
            this.$router.push('/admin/venues');
        })
          .catch((error) => {
            console.error('Error adding venue:', error);
          });
      },
    },
  };
  </script>
  