<template>
  <div>
    <div class="stat-item mb-5">
      <p>Total Messages: {{ statistics.total_messages }}</p>
      <p>Average Messages: {{ statistics.average_messages_per_day.toFixed(2) }}</p>
      <p class="text-xs">per day of chatting</p>
      <p>Longest Conversation: {{ statistics.longest_conversation }}</p>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-0">Percentage Rate</h2><p class="mt-[-5px]">(Largest First):</p>
      <ul>
        <li v-for="(percentage, user) in sortedUserPercentages" :key="user">
          {{ user }} - {{ percentage.toFixed(2) }}% ({{ statistics.user_message_counts[user] }} messages)
        </li>
      </ul>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-0">Average Response Times</h2><p class="mt-[-5px]">(Quickest First):</p>
      <ul>
        <li v-for="(time, user) in sortedAverageResponseTimes" :key="user">
          {{ user }} - {{ formatTime(time) }}
        </li>
      </ul>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-2">Top 10 Most Active Days:</h2>
      <ul>
        <li v-for="(day, index) in statistics.top_10_days" :key="index">
          {{ day[0] }} - {{ day[1] }} messages
        </li>
      </ul>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-2">Laugh Expressions Counter:</h2>
      <p>{{ statistics.laugh_count }}</p>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-2">Swear Words Statistics:</h2>
      <p>Total Swears: {{ statistics.swear_count }}</p>
      <p>Swear Rate: {{ statistics.swear_rate.toFixed(2) }}%</p>
      <ul>
        <li v-for="([count, swears], index) in sortedGroupedSwearFrequencies" :key="index">
          {{ count }}: {{ swears.join(', ') }}
        </li>
      </ul>
    </div>

    <div class="stat-item mb-5">
      <h2 class="text-xl font-medium mb-2 cursor-pointer" @click="toggleSwearWordsVisibility">Suggested New Swear Words:</h2>
      <ul v-if="showSuggestedSwears">
        <li v-for="(swear, index) in statistics.suggested_swears" :key="index">
          {{ swear }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatItems',
  props: {
    statistics: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showSuggestedSwears: false,
    };
  },
  computed: {
    sortedGroupedSwearFrequencies() {
      return this.statistics.sorted_grouped_swear_frequencies;
    },
    sortedUserPercentages() {
      return Object.entries(this.statistics.user_percentages)
        .sort(([, a], [, b]) => b - a)
        .reduce((acc, [key, value]) => {
          acc[key] = value;
          return acc;
        }, {});
    },
    sortedAverageResponseTimes() {
      return Object.entries(this.statistics.average_response_times)
        .sort(([, a], [, b]) => a - b)
        .reduce((acc, [key, value]) => {
          acc[key] = value;
          return acc;
        }, {});
    },
  },
  methods: {
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}m ${remainingSeconds}s`;
    },
    toggleSwearWordsVisibility() {
      this.showSuggestedSwears = !this.showSuggestedSwears;
    },
  },
};
</script>

<style scoped>
.stat-item {
  margin-bottom: 1.25rem;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
