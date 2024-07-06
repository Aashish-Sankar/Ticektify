<template>
    <div>
        <userNav/>
        <div class = 'form-container'>
      <section class="form">
        <h2 class="text-center">&nbsp;&nbsp;Buy Ticket&nbsp;&nbsp;</h2>
        <form @submit.prevent="submitBooking">
          <br />
          <div v-if="screening">
            <div>
              <label>{{ screening.show.name }}: </label>
              <select v-model="selectedScreening" id="screening" name="screening">
                <option v-for="proj in screenings" :key="proj.id" :value="proj.id">
                  <b>Day:</b> {{ formatDate(proj.day) }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <b>Time:</b> {{ formatTime(proj.time) }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <b>Venue:</b> {{ proj.venue.name }}
                </option>
              </select>
            </div>
            <div>
              <label><br />Number of seats: <br /></label>
              <select v-model="selectedSeats" id="seats" name="seats" @change="updateTotalCost">
                <option v-for="i in seatsRange" :key="i" :value="i" selected=0>{{ i }}</option>
              </select>
            </div>
            <br />
            <div>
              <label>Total Cost (Each ticket: {{ screening.show.price }}): </label>
              <input id="price" name="totalPrice" :value="totalCost" readonly />
            </div>
            <br />
            <div>
                <br/>
              <button class="submit" type="submit">Buy</button>
            </div>
          </div>
        </form>
      </section>
    </div>
    </div>
  </template>
  
  <script>
  import UserNav from "../components/UserNav";
  export default {
    components:{
        userNav: UserNav,
    },
    data() {
      return {
        screening: null,
        screenings: [],
        selectedScreening: null,
        selectedSeats: 1,
        totalCost: 0,
        seatsRange: 10,
        access_token: localStorage.getItem('access_token'),
      };
    },
    async mounted() {
      await this.fetchScreenings();
    },
    methods: {
      async fetchScreenings() {
        try {
            const id = this.$route.params.id;
            var response = '';
            if (id != null){
          response = await fetch(`http://localhost:8000/api/booking/${id}`, {
            headers: {
              Authorization: `Bearer ${this.access_token}`,
            },
          });
        } else {
          response = await fetch('http://localhost:8000/api/booking', {
            headers: {
              Authorization: `Bearer ${this.access_token}`,
            },
          });
        }
    
          const data = await response.json();
          this.screening = data.screening;
          this.screenings = data.screenings;
          this.selectedScreening = this.screening ? this.screening.id : null;
          this.updateTotalCost();
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US");
      },
      formatTime(timeString) {
        const time = new Date(`1970-01-01T${timeString}`);
        return time.toLocaleTimeString("en-US", {
          hour: "numeric",
          minute: "numeric",
          hour12: true,
        });
      },
      updateTotalCost() {
        this.totalCost = this.selectedSeats * this.screening.show.price;
      },
      async submitBooking() {
        const newBooking = {
            screening: this.selectedScreening,
            seats: this.selectedSeats,
            totalPrice: this.totalCost,
        };
        console.log(JSON.stringify(newBooking))
  try {
    const response = await fetch('http://localhost:8000/api/booking', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.access_token}`,
      },
      body: JSON.stringify(newBooking),
    });
    const data = await response.json();
    
    console.log(data)
    if (response.ok) {
      if(data.message){
        console.log(data.message);
        alert(data.message);
        this.$router.push('/user/home');
      }else{
        alert(data.error);
      }
        
      
    } else {
      console.error("Error submitting booking:", data.error);
      alert(data.error);
    }
  } catch (error) {
    console.error("Error submitting booking:", error);
    alert("An error occurred while submitting the booking.");
  }
},

    },
  };
  </script>
  
