<template>
    <div>
        <adminNav />
      <br />
      <h1 style="text-align: center;">SHOWS</h1>
      <br />
      <div class="container px-2 py-1">
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 card-deck">
        <div v-for="show in shows" :key="show.id" class="col">
          <div class="card h-auto">
            <img class="card-img-top img-fluid" :src= show.img :alt="show.name">
            <div class="card-body">
              <p></p>
              <p>Name: {{ show.name }}</p>
              <p>Rating: {{ show.rating }}</p>
              <p>Price: {{ show.price }}</p>
              <p>Tags: {{ show.tags }}</p>
              <p>
                <a
                  href="#"
                  @click="deleteShow(show.id)"
                  >Delete</a
                > |
                <router-link :to="{ name: 'editShow', params: { id: show.id }}">Edit</router-link>
              </p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100 splcard">
            <router-link :to= "{ name:'showAdd' }" class="button">
              <img src="https://cdn-icons-png.flaticon.com/512/8191/8191584.png" width="50" height="50">
            </router-link>
          </div>
        </div>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import AdminNav from "../components/AdminNav";
  export default {
    components: {
      adminNav: AdminNav,
    },
    data() {
      return {
        shows: [],
      };
    },
    created() {
      this.fetchData();
    },
    methods: {
      fetchData() {
        fetch("http://127.0.0.1:8000/api/admin/shows", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            this.shows = data;
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      },
      deleteShow(id) {
        const confirmed = window.confirm("Are you sure you want to delete this item?");
        if (confirmed) {
          fetch(`http://127.0.0.1:8000/api/admin/show_delete/${id}`, {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data);
              this.fetchData();
            })
            .catch((error) => {
              console.error("Error deleting show:", error);
            });
        }
      },
    },
  };
  </script>

<style>

.card-img-top {
  display: block;
  margin-left: auto;
  margin-right: auto;
    width: 40% !important;
    height: 25% !important;
    object-fit: cover !important;
}

.card-deck {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
}

.card {
  flex: 1 0 auto;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: rgb(243, 215, 180);
}

.form {
  width: 100%;
  max-width: 500px;
  padding: 20px;
  border: 5px solid #000000;
  border-radius: 5px;
  background-color: rgb(236, 235, 203);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.form h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form label {
  font-weight: bold;
}

.form .form-group {
  margin-bottom: 20px;
}

.form .form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: inset 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.form button[type="submit"] {
  background-color: #ffffff !important;
  color: #000000;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  text-align: center;
}

.form button[type="submit"]:hover {
  background-color: #b4b5b5 !important;
}

</style>