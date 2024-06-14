<template>
  <div class="chart-container">
    <h2>Messages by Month</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'MessagesByMonthChart',
  components: {
    Bar
  },
  props: {
    messagesByMonth: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      const monthOrder = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ];
      const labels = monthOrder;
      const data = labels.map(month => this.messagesByMonth[month] || 0);
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
              text: 'Month'
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
