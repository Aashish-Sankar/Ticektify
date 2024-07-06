<template>
    <div>
    <adminNav/>
    <div class = 'form-container'  style="align-content: center">
        <div class = 'form'>
      <h3 style="text-align: center;">Admin Login</h3>
      <br/>
      <form @submit.prevent="loginAdmin">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input v-model="email" type="email" class="form-control" id="email" name="email" placeholder="Enter email" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" name="password" placeholder="Enter Password" />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</div>
</div>
  </template>
  
  <script>
  import AdminNav from "../components/AdminNav"
export default {
  components:{
      adminNav : AdminNav
  },
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      access_token: ''
    };
  },
  methods: {
    async loginAdmin() {
      try {
        const response = await fetch('http://localhost:8000/api/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.access_token}`
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();
        if (response.ok) {
          if(data.message != undefined){
            console.log(data.user)
            this.access_token = data.access_token;
            localStorage.setItem('access_token', this.access_token);
            localStorage.setItem('user_role', data.user.role);
            console.log(localStorage.getItem('user_role'))
              alert(data.message);
              this.$router.push('/admin/home');
          }else{
              alert(data.error);
          }
        } else {
          this.errorMessage = data.error;
        }
      } catch (error) {
        console.error('Error logging in:', error);
        this.errorMessage = 'An error occurred while logging in.';
      }
    }
  }
};
  </script>
  
  <style>
  .error-message {
    color: red;
    margin-top: 10px;
  }
  </style>
  