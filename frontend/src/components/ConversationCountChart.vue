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
  name: 'ConversationCountChart',
  props: {
    conversations: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const canvas = ref(null);

    onMounted(() => {
      const ctx = canvas.value.getContext('2d');
      const data = props.conversations;

      const dates = data.map(conv => conv.start_time);
      const conversationCounts = dates.reduce((counts, date) => {
        const day = date.split('T')[0];
        counts[day] = (counts[day] || 0) + 1;
        return counts;
      }, {});

      const labels = Object.keys(conversationCounts).sort();
      const counts = labels.map(date => conversationCounts[date]);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Number of Conversations',
            data: counts,
            backgroundColor: 'rgba(0, 0, 0, 1)',
            borderColor: 'rgba(50, 50, 50, 1)',
            borderWidth: 1,
            fill: true,
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
                text: 'Date',
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
  height: 60vh;
  width: 100%;
}
</style>
