<template>
    <div class="form-container">
    <section class="form">
      <br />
      <h2 style="text-align: center;">Edit Venue</h2>
      <form @submit.prevent="editVenue">
        <br />
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" v-model="name" class="form-control" id="name" required />
        </div>
        <div class="form-group">
          <label for="capacity">Capacity</label>
          <input type="text" v-model="capacity" class="form-control" id="capacity" required />
        </div>
        <div class="form-group">
          <label for="place">City</label>
          <input type="text" v-model="place" class="form-control" id="place" required />
        </div>
        <div class="form-group">
          <label for="location">Location</label>
          <input type="text" v-model="location" class="form-control" id="location" required />
        </div>
        <br />
        <button type="submit" class="btn btn-primary">Edit</button>
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
        place: '',
        location: '',
        access_token: localStorage.getItem('access_token'),
      };
    },
    created() {
      this.fetchData();
    },
    methods: {
      fetchData() {
        const id = this.$route.params.id;
  
        fetch(`http://localhost:8000/api/admin/venue_edit/${id}`, {
        headers: {
          Authorization: `Bearer ${this.access_token}`,
        },
      })
          .then((response) => response.json())
          .then((data) => {
            this.name = data.name;
            this.capacity = data.capacity;
            this.place = data.place;
            this.location = data.location;
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
      },
      editVenue() {
        const formData = {
          name: this.name,
          capacity: this.capacity,
          place: this.place,
          location: this.location,
        };
        const id = this.$route.params.id;
  
        fetch(`http://localhost:8000/api/admin/venue_edit/${id}`, {
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
            this.$router.push('/admin/venues');
          })
          .catch((error) => {
            console.error('Error editing venue:', error);
          });
      },
    },
  };
  </script>
  