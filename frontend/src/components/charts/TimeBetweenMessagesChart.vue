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
  name: 'TimeBetweenMessagesChart',
  props: {
    timeDifferences: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const canvas = ref(null);

    onMounted(() => {
      const ctx = canvas.value.getContext('2d');
      const data = props.timeDifferences;

      const binEdges = [0, 3, 5, 10, 30, 60, 120, 300, 600, 1800, 3600, 7200, 14400, 28800, 86400, 172800, 604800, 1209600];
      const labels = [];
      const histogramData = new Array(binEdges.length - 1).fill(0);

      data.forEach(time => {
        for (let i = 0; i < binEdges.length - 1; i++) {
          if (time >= binEdges[i] && time < binEdges[i + 1]) {
            histogramData[i] += 1;
            break;
          }
        }
      });

      for (let i = 0; i < binEdges.length - 1; i++) {
        let label;
        if (binEdges[i] < 60) {
          label = `${binEdges[i]}-${binEdges[i + 1]} sec`;
        } else if (binEdges[i] < 3600) {
          label = `${Math.floor(binEdges[i] / 60)}-${Math.floor(binEdges[i + 1] / 60)} min`;
        } else if (binEdges[i] < 86400) {
          label = `${Math.floor(binEdges[i] / 3600)}-${Math.floor(binEdges[i + 1] / 3600)} hr`;
        } else {
          label = `${Math.floor(binEdges[i] / 86400)}-${Math.floor(binEdges[i + 1] / 86400)} days`;
        }
        labels.push(label);
      }

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Number of Messages',
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
                text: 'Number of Messages',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Time Interval',
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
