<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'MessagesByHourChart',
  components: {
    Bar
  },
  props: {
    messagesByHour: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      const labels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
      const data = labels.map((label, index) => this.messagesByHour[index] || 0);
      return {
        labels,
        datasets: [
          {
            label: 'Messages',
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
              text: 'Number of Messages'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Hour of the Day'
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
  height: 90%;
  width: 100%;
}
</style>
