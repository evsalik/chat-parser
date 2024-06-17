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
  name: 'CommonWordsChart',
  components: {
    Bar
  },
  props: {
    commonWords: {
      type: Array,
      required: true,
    },
  },
  computed: {
    chartData() {
      const topCommonWords = this.commonWords.slice(0, 150);
      const labels = topCommonWords.map(([word]) => word);
      const data = topCommonWords.map(([word, count]) => count);
      return {
        labels,
        datasets: [
          {
            label: 'Occurrences',
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
              text: 'Occurrences'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Words'
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
