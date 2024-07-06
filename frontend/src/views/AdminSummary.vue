<template>
    <div>
        <adminNav/>
    <div class="line-graph">
        <h2 style="text-align: center; text-decoration: double;">Bookings Made Previous Week</h2>
        <br/>
      <apexchart :options="chartOptions" :series="chartSeries" type="line" />
    </div>
    </div>
  </template>
  
  <script>
  import AdminNav from '../components/AdminNav'
  import VueApexCharts from "vue3-apexcharts";
  
  export default {
    components: {
      apexchart: VueApexCharts,
      adminNav : AdminNav
    },
    data() {
      return {
        chartOptions: {
          chart: {
            background: "#1e1e1e",
            foreColor: "#ffffff",
            height: 100,
            width: 100,
            type: "line",
          },
          xaxis: {
            type: "datetime",
            labels: {
                style: {
                    colors: "#ffffff",
                },
            },
          },
          yaxis: {
        labels: {
          style: {
            colors: "#ffffff",
          },
        },
      },
      markers: {
        colors: "#ffffff",
      },
      tooltip: {
        theme: "dark",
      },
        },
        chartSeries: [],
        access_token: localStorage.getItem('access_token'),
      };
    },
    mounted() {
      this.fetchChartData();
    },
    methods: {
      async fetchChartData() {
        try {
          const response = await fetch("http://localhost:8000/api/admin/summary", {
          headers: {
            Authorization: `Bearer ${this.access_token}`,
          },
        });
          const data = await response.json();
          console.log(data)
          this.chartSeries = [
            {
              name: "Bookings",
              data: data.bookings,
            },
          ];
          console.log(this.chartSeries)
        } catch (error) {
          console.error("Error fetching chart data:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .line-graph {
    margin: 20px;
  }
  </style>
  