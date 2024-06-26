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
  name: 'MessageLengthDistributionByUser',
  props: {
    userMessageLengths: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const canvas = ref(null);

    onMounted(() => {
      const ctx = canvas.value.getContext('2d');
      const data = Object.keys(props.userMessageLengths).map(user => {
        const lengths = props.userMessageLengths[user];
        return {
          user,
          averageLength: lengths.reduce((acc, len) => acc + len, 0) / lengths.length,
        };
      });

      data.sort((a, b) => b.averageLength - a.averageLength);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(d => d.user),
          datasets: [{
            label: 'Average Message Length',
            data: data.map(d => d.averageLength),
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
                text: 'Average Message Length',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Users',
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
