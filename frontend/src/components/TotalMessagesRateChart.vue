<template>
  <div class="chart-container">
    <h2>User Message Count Chart</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'TotalMessagesRateChart',
  components: {
    Bar
  },
  props: {
    userMessageCounts: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      console.log("User Message Counts:", this.userMessageCounts)
      return {
        labels: Object.keys(this.userMessageCounts),
        datasets: [
          {
            label: 'Message Count',
            backgroundColor: '#000000',
            data: Object.values(this.userMessageCounts)
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Message Count'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Users'
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  height: 40vh;
  width: 40vw;
}
</style>
