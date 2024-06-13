<template>
  <div class="chart-container">
    <h2>First Messages Per Day</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'FirstMessagesChart',
  components: {
    Bar
  },
  props: {
    firstMessageCount: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      const labels = Object.keys(this.firstMessageCount).sort();
      const data = labels.map(user => this.firstMessageCount[user]);
      return {
        labels,
        datasets: [
          {
            label: 'First Messages',
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
              text: 'Number of First Messages'
            }
          },
          x: {
            title: {
              display: true,
              text: 'User'
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
  position: relative;
  height: 60vh;
  width: 10%;
}
</style>
