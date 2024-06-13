<template>
  <div>
    <h1>Chat Statistics</h1>
    <div v-if="statistics">
      <p>Total Messages: {{ statistics.total_messages }}</p>
      <p>Most active user: {{ statistics.most_active_user[0] }}</p>
      <h2>Percentage Rate:</h2>
      <ul>
        <li v-for="(percentage, user) in statistics.user_percentages" :key="user">
          {{ user }} - {{ percentage.toFixed(2) }}% ({{ statistics.user_message_counts[user] }} messages)
        </li>
      </ul>
      <TotalMessagesRateChart :userMessageCounts="statistics.user_message_counts" />
      <CommonWordsList :commonWords="statistics.word_frequencies" />
      <CommonWordsChart :commonWords="statistics.word_frequencies" />
    </div>
    <div v-else>
      <p>Loading statistics...</p>
    </div>
  </div>
</template>

<script>
import TotalMessagesRateChart from './TotalMessagesRateChart.vue';
import CommonWordsList from './CommonWordsList.vue';
import CommonWordsChart from './CommonWordsChart.vue';

export default {
  components: {
    TotalMessagesRateChart,
    CommonWordsList,
    CommonWordsChart,
  },
  props: {
    statistics: {
      type: Object,
      required: false,
      default: () => ({}),
    },
  },
  created() {
    const stats = this.$route.query.statistics;
    if (stats) {
      this.statistics = JSON.parse(stats);
    }
    console.log("Statistics in created:", this.statistics);  // Debugging line
  },
  data() {
    return {
      statistics: {}
    };
  }
};
</script>

<style>
</style>
