<template>
  <div>
    <canvas id="messageLengthChart"></canvas>
    <p>fyi 58 chars is a length of a youtube shorts link =)</p>
  </div>
</template>

<script>
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default {
  props: {
    statistics: {
      type: Object,
      required: true
    }
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const ctx = document.getElementById('messageLengthChart').getContext('2d');
      const data = this.statistics.message_length_distribution;

      const filteredData = Object.keys(data).reduce((acc, key) => {
        if (key !== '0') {
          acc[key] = data[key];
        }
        return acc;
      }, {});

      const labels = Object.keys(filteredData).map(length => `${length} chars`);
      const values = Object.values(filteredData);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Messages',
            data: values,
            backgroundColor: 'black',
            borderColor: 'black',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
canvas {
  background-color: white;
  height: 90%;
  width: 100%;
}
</style>
