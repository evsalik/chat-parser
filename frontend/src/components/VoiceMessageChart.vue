<template>
  <div class="chart-container">
    <h2>User Voice Message Counts</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'VoiceMessageChart',
  components: {
    Bar
  },
  props: {
    voiceMessageCounts: {
      type: Object,
      required: true,
    },
  },
  computed: {
    chartData() {
      const sortedEntries = Object.entries(this.voiceMessageCounts).sort((a, b) => b[1] - a[1]);
      const labels = sortedEntries.map(entry => entry[0]);
      const data = sortedEntries.map(entry => entry[1]);
      return {
        labels,
        datasets: [
          {
            label: 'Voice Messages',
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
              text: 'Voice Messages'
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
  position: relative;
  height: 60vh;
  width: 100%;
}
</style>
