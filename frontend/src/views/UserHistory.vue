<template>
    <section>
       <userNav/>
      <br />
      <h2>&nbsp;&nbsp;Current Bookings&nbsp;&nbsp;</h2>
      <user-bookings v-if="nowBookings.length > 0" :bookings="nowBookings" />
      <p v-else style="text-align: center">YOU DON'T HAVE ANY BOOKINGS.</p>
      <br />
      <h2>&nbsp;&nbsp;Past Bookings&nbsp;&nbsp;</h2>
      <user-bookings v-if="pastBookings.length > 0" :bookings="pastBookings" />
      <p v-else style="text-align: center">YOU DON'T HAVE PAST BOOKINGS.</p>
    </section>
  </template>
  
  <script>
  import UserBookings from '../components/UserBookings';
  import UserNav from '../components/UserNav';
  
  export default {
    components: {
      UserBookings,
      userNav: UserNav,
    },
    data() {
      return {
        nowBookings: [],
        pastBookings: [],
        access_token: localStorage.getItem('access_token'),
      };
    },
    async mounted() {
      await this.fetchUserBookings();
    },
    methods: {
      async fetchUserBookings() {
        try {
          const response = await fetch('http://localhost:8000/api/user/bookings', {
          headers: {
            Authorization: `Bearer ${this.access_token}`,
          },
        });
          const data = await response.json();
          this.nowBookings = data.now_bookings;
          this.pastBookings = data.past_bookings;
        } catch (error) {
          console.error('Error fetching user bookings:', error);
        }
      },
    },
  };
  </script>

  