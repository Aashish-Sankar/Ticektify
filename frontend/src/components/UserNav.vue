<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/user/home">
          <h3><b>Ticketify</b></h3>
        </a>
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ show: isNavbarOpen }" id="navbar">
          <ul class="navbar-nav ms-auto">
            <li v-if="isAuthenticated">
              <a class="nav-item nav-link" href="/user/home">Dashboard</a>
            </li>
            <li v-if="isAuthenticated">
              <a class="nav-item nav-link" href="/user/bookings">Bookings</a>
            </li>
            <li v-if="isAuthenticated">
              <a class="nav-item nav-link" @click="logout">Logout</a>
            </li>
            <li v-if="isAuthenticated">
              <search-form></search-form>
            </li>
            <li v-if="!isAuthenticated">
              <a class="nav-item nav-link" href="/user/login">Login</a>
            </li>
            <li v-if="!isAuthenticated">
              <a class="nav-item nav-link" href="/user/signUp">Sign Up</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
import SearchForm from './SerachForm'; 
import jwt_decode from 'jwt-decode';
export default {
  name: 'userNav',
  components: {
    'search-form': SearchForm,
  },
  data() {
      return {
        isNavbarOpen: false,
        isAuthenticated :null,
        message: ""
      };
    },
    methods: {
      toggleNavbar() {
        this.isNavbarOpen = !this.isNavbarOpen;
      },verifyToken(token) {
  try {
    const decoded = jwt_decode(token);
    return decoded;
  } catch (error) {
    return null;
  }
},
      isUserAuthenticated(){
        const access_token = localStorage['access_token']
        const decodedToken = this.verifyToken(access_token)
        console.log(access_token)
        if(access_token != 'null' && decodedToken && decodedToken.exp * 1000 > Date.now()){
          this.isAuthenticated = true;
          console.log(this.isAuthenticated)
      } else {
        this.isAuthenticated=false;
        console.log(this.isAuthenticated)
      }
    },
    logout(){
      fetch(`http://localhost:8000/api/user/logout`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
      }).then((response) => response.json())
          .then((data) => {
            console.log(data)
            if (data.message != undefined){
              this.message = data.message;
              alert(this.message)
              localStorage.setItem("access_token", 'null');
              localStorage.setItem('user_role', 'null');
              this.$router.push('/user/login');
            }
            else{
              alert(data.error)
            }
            
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      
    }
  },
  mounted(){
    this.isUserAuthenticated();
  }
}
  </script>
  
  <style>
  .nav-link {
    list-style: none !important;
    color: white !important;
  }
  
  .nav-link:hover {
    color: grey !important;
  }
  </style>
  