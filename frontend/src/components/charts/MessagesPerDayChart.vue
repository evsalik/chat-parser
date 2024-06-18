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
  name: 'MessagesPerDayChart',
  components: {
    Bar
  },
  props: {
    messagesPerDay: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      const labels = Object.keys(this.messagesPerDay).sort();
      const data = labels.map(date => this.messagesPerDay[date]);
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
              text: 'Date'
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
  margin: auto;
  height: 90%;
  width: 100%;
}
</style>
