<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default defineComponent({
  name: 'ConversationLengthsChart',
  props: {
    sortedConversationLengths: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const canvas = ref(null);

    onMounted(() => {
      const ctx = canvas.value.getContext('2d');
      const data = props.sortedConversationLengths;

      const binEdges = [1, 2, 5, 10, 20, 30, 50, 75, 100, 133, 167, 200, 250, 300, 400, 500, 750, 1000, 2000];
      const labels = [];
      const histogramData = new Array(binEdges.length - 1).fill(0);

      data.forEach(length => {
        for (let i = 0; i < binEdges.length - 1; i++) {
          if (length >= binEdges[i] && length < binEdges[i + 1]) {
            histogramData[i] += 1;
            break;
          }
        }
      });

      // Create labels for bins
      for (let i = 0; i < binEdges.length - 1; i++) {
        labels.push(`${binEdges[i]}-${binEdges[i + 1]}`);
      }

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Number of Conversations',
            data: histogramData,
            backgroundColor: 'rgba(0, 0, 0, 1)',
            borderColor: 'rgba(0, 0, 0, 1)',
            borderWidth: 1,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Conversations',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Conversation Length (Messages)',
              },
              ticks: {
                maxRotation: 90,
                minRotation: 90,
              },
            },
          },
        },
      });
    });

    return {
      canvas,
    };
  },
});
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 90%;
  width: 100%;
}
</style>
