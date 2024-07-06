<template>
    <div>
        <userNav/>
        <br/>
        <div class="form-container">
            <div class="form">
      <h3 style="text-align: center;">User Sign Up</h3>
      <br/>
      <form @submit.prevent="signupUser">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input v-model="email" type="email" class="form-control" id="email" name="email" placeholder="Enter email" />
        </div>
        <br/>
        <div class="form-group"> 
          <label for="firstName">First Name</label>
          <input v-model="firstName" type="text" class="form-control" id="firstName" name="firstName" placeholder="Enter First Name" />
        </div>
        <br/>
        <div class="form-group">
          <label for="password1">Password</label>
          <input v-model="password1" type="password" class="form-control" id="password1" name="password1" placeholder="Enter Password " />
        </div>
        <br/>
        <div class="form-group">
          <label for="password2">Password Confirm</label>
          <input v-model="password2" type="password" class="form-control" id="password2" name="password2" placeholder="Confirm Password " />
        </div>
        <br/>
        <div class="form-group">
          <div>
            <input type="radio" name="role" value="user" id="user" required />
            <label for="user">I am a User</label>
          </div>
          <br/>
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</div>
</div>
  </template>
  
  <script>
  import UserNav from "../components/UserNav";
  export default {
    components:{
        userNav : UserNav
    },
    data() {
      return {
        email: '',
        firstName: '',
        password1: '',
        password2: '',
        errorMessage: '',
        access_token: '',
      };
    },
    methods: {
      async signupUser() {
        try {
          const response = await fetch('http://localhost:8000/api/user/signUp', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: this.email,
              firstName: this.firstName,
              password1: this.password1,
              password2: this.password2,
              role: 'user'
            })
          });
  
          const data = await response.json();
  
          if (response.ok) {
            if (data.message) {
              alert(data.message);
              this.$router.push('/user/login');
            } else {
                this.errorMessage = data.error;
            }
          } else {
            this.errorMessage = data.error;
          }
        } catch (error) {
          console.error('Error signing up:', error);
          this.errorMessage = 'An error occurred while signing up.';
        }
      }
    }
  };
  </script>
  