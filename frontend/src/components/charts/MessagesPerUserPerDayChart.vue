<template>
  <div class="chart-container">
    <canvas id="messagesPerUserPerDayChart"></canvas>
  </div>
</template>

<script>
import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale } from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale);

export default {
  props: {
    statistics: Object
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const ctx = document.getElementById('messagesPerUserPerDayChart').getContext('2d');
      const data = this.statistics.messages_per_user_per_day;

      const labels = Object.keys(data[Object.keys(data)[0]]);
      const datasets = Object.keys(data).map((user, index) => ({
        label: user,
        data: Object.values(data[user]),
        fill: false,
        borderColor: this.getGrayShade(index),
        backgroundColor: this.getGrayShade(index),
        borderWidth: 2,
        pointRadius: 3,
        pointBackgroundColor: this.getGrayShade(index),
      }));

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            legend: {
              labels: {
                color: '#000'
              }
            }
          }
        }
      });
    },
    getGrayShade(index) {
      const shade = Math.floor(50 + (index * 50) % 200).toString(16).padStart(2, '0');
      return `#${shade}${shade}${shade}`;
    }
  }
};
</script>

<style scoped>
.chart-container {
  position: relative;
  margin: 20px 0;
  height: 90%;
  width: 100%;
}
</style>
