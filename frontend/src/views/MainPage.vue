<template>
    <div id="app">
      <section id="team">
        <div class="container my-3 py-5 text-center">
          <div class="row mb-5">
            <div class="col">
              <h1>TICKETIFY</h1>
              <p class="mt-3">Book it on the go!</p>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-4 col-md-4">
              <div class="card">
                <div class="card-body">
                  <h3>User</h3>
                  <button type="submit" class="btn">
                    <router-link to="/user/signup"><h5>Sign Up</h5></router-link>
                  </button>
                </div>
              </div>
            </div>
            <br/>
            <div class="col-lg-4 col-md-4">
              <div class="card">
                <div class="card-body">
                  <h3>User</h3>
                  <button type="submit" class="btn">
                    <router-link to="/user/login"><h5>Login</h5></router-link>
                  </button>
                </div>
              </div>
            </div>
            <br/>
            <div class="col-lg-4 col-md-4">
              <div class="card">
                <div class="card-body">
                  <h3>Admin</h3>
                  <button type="submit" class="btn">
                    <router-link to="/admin/login"><h5>Login</h5></router-link>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: "MainPage",
  };
  </script>
  
  <style>
  @import '../assets/mainpage.css'
  </style>
  