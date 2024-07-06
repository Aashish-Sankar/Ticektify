<template>
    <div class="form-container">
    <section class="form">
      <br />
      <h2 style="text-align: center;">Edit Show</h2>
      <form @submit.prevent="editShow">
        <br />
        <div class="form-group">
          <label for="img">Image</label>
          <input
            type="text"
            v-model="currentData.img"
            class="form-control"
            id="img"
            placeholder="Poster Link"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="name">Name</label>
          <input
            type="text"
            v-model="currentData.name"
            class="form-control"
            id="name"
            placeholder="Show Name"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="rating">Rating</label>
          <input
            type="text"
            v-model="currentData.rating"
            class="form-control"
            id="rating"
            placeholder="Enter Rating"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="price">Price</label>
          <input
            type="text"
            v-model="currentData.price"
            class="form-control"
            id="price"
            placeholder="Enter Price"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="tags">Tags</label>
          <input
            type="text"
            v-model="currentData.tags"
            class="form-control"
            id="tags"
            placeholder="Enter Tags"
          />
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
        currentData: {
          img: "",
          name: "",
          rating: "",
          price: "",
          tags: "",
        },
        access_token: localStorage.getItem('access_token'),
      };
    },
    created() {
      this.fetchData();
    },
    methods: {
      fetchData() {
        const id = this.$route.params.id;
  
        fetch(`http://localhost:8000/api/admin/show_edit/${id}`, {
        headers: {
          Authorization: `Bearer ${this.access_token}`,
        },
      })
          .then((response) => response.json())
          .then((data) => {
            this.currentData = {
              img: data.img,
              name: data.name,
              rating: data.rating,
              price: data.price,
              tags: data.tags,
            };
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      },
      editShow() {
        const formData = {
          img: this.currentData.img,
          name: this.currentData.name,
          rating: this.currentData.rating,
          price: this.currentData.price,
          tags: this.currentData.tags,
        };
        const id = this.$route.params.id;
  
        fetch(`http://localhost:8000/api/admin/show_edit/${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.access_token}`,
          },
          body: JSON.stringify(formData),
        })
          .then((response) => response.json())
          .then((data) => {
           console.log(data);
            alert("Show edited successfully!");
            this.$router.push({ name: "adminShow" });
          })
          .catch((error) => {
            console.error("Error editing show:", error);
          });
      },
    },
  };
  </script>
  