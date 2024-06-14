<template>
  <div class="chart-container">
    <h2>Messages by Hour of the Day</h2>
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
      const labels = Object.keys(this.messagesByHour).sort((a, b) => a - b);
      const data = labels.map(hour => this.messagesByHour[hour]);
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
  margin-top: 4vw;
  position: relative;
  height: 60vh;
  width: 100%;
}
</style>
