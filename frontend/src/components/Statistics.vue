<template>
  <div>
    <h1>Chat Statistics</h1>
    <div v-if="statistics">
      <p>Total Messages: {{ statistics.total_messages }}</p>
    </div>
    <div v-else>
      <p>Loading statistics...</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    statistics: {
      type: Object,
      required: false,
      default: () => ({}),
    },
  },
  created() {
    // Parse statistics from query parameters
    const stats = this.$route.query.statistics;
    if (stats) {
      this.statistics = JSON.parse(stats);
    }
    console.log("Statistics:", this.statistics);  // Debugging line
  },
  data() {
    return {
      statistics: {}
    };
  }
};
</script>

<style>
/* Add your styles here */
</style>
