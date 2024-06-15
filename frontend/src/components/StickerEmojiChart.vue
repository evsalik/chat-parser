<template>
  <div class="chart-container">
    <h2>Sticker Emoji Popularity</h2>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'StickerEmojiChart',
  components: {
    Bar
  },
  props: {
    stickerEmojiCounts: {
      type: Object,
      required: true,
    },
  },
  computed: {
    chartData() {
      const labels = Object.keys(this.stickerEmojiCounts);
      const data = Object.values(this.stickerEmojiCounts);
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
              text: 'Stickers'
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
