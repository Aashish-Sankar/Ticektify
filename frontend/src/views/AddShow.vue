<template>
<div class="form-container">
    <section class="form">
      <br />
      <h2 style="text-align: center;">Add Show</h2>
      <form @submit.prevent="addShow">
        <br />
        <div class="form-group">
          <label for="img">Image</label>
          <input type="text" v-model="img" class="form-control" id="img" placeholder="Poster Link" required />
        </div>
        <br />
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" v-model="name" class="form-control" id="name" placeholder="Show Name" required />
        </div>
        <br />
        <div class="form-group">
          <label for="rating">Rating</label>
          <input type="text" v-model="rating" class="form-control" id="rating" placeholder="Enter Rating" required />
        </div>
        <br />
        <div class="form-group">
          <label for="price">Price</label>
          <input type="text" v-model="price" class="form-control" id="price" placeholder="Enter Price" required />
        </div>
        <br />
        <div class="form-group">
          <label for="tags">Tags</label>
          <input type="text" v-model="tags" class="form-control" id="tags" placeholder="Enter Tags" required />
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
        img: '',
        name: '',
        rating: '',
        price: '',
        tags: '',
        access_token: localStorage.getItem('access_token'),
      };
    },
    methods: {
      addShow() {
        const formData = {
          img: this.img,
          name: this.name,
          rating: this.rating,
          price: this.price,
          tags: this.tags
        };
  
        fetch('http://localhost:8000/api/admin/show_add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.access_token}`,
          },
          body: JSON.stringify(formData)
        })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            this.$router.push('/admin/shows');
          })
          .catch(error => {
            console.error('Error adding show:', error);
          });
      }
    }
  };
  </script>
  