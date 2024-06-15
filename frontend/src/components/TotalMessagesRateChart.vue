<template>
  <div class="chart-container">
    <h2>User Message Count Chart</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

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
      const sortedEntries = Object.entries(this.userMessageCounts).sort((a, b) => b[1] - a[1]);
      const labels = sortedEntries.map(entry => entry[0]);
      const data = sortedEntries.map(entry => entry[1]);
      return {
        labels,
        datasets: [
          {
            label: 'Message Count',
            backgroundColor: '#000000',
            data,
          },
        ],
      };
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
            },
            ticks: {
              maxRotation: 90,
              minRotation: 90
            }
          }
        }
      };
    }
  }
};
</script>

<style scoped>
.chart-container {
  height: 40vh;
  width: 100%;
}
</style>
