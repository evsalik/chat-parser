<template>
  <div>
    <h1>Chat Statistics</h1>
    <div v-if="statistics">
      <p>Total Messages: {{ statistics.total_messages }}</p>
      <p>Average Messages per Day: {{ statistics.average_messages_per_day.toFixed(2) }}</p>

      <h2>Percentage Rate (Largest First):</h2>
      <ul>
        <li v-for="(percentage, user) in sortedUserPercentages" :key="user">
          {{ user }} - {{ percentage.toFixed(2) }}% ({{ statistics.user_message_counts[user] }} messages)
        </li>
      </ul>

      <h2>Average Response Times (Quickest First):</h2>
      <ul>
        <li v-for="(time, user) in sortedAverageResponseTimes" :key="user">
          {{ user }} - {{ formatTime(time) }}
        </li>
      </ul>

      <TotalMessagesRateChart :userMessageCounts="statistics.user_message_counts" />
      <CommonWordsList :commonWords="statistics.word_frequencies" />
      <CommonWordsChart :commonWords="statistics.word_frequencies" />
      <MessagesPerDayChart :messagesPerDay="statistics.messages_per_day" />

      <h2>Top 10 Most Active Days:</h2>
      <ul>
        <li v-for="(day, index) in statistics.top_10_days" :key="index">
          {{ day[0] }} - {{ day[1] }} messages
        </li>
      </ul>

      <MessagesPerWeekChart :messagesPerWeek="statistics.messages_per_week" />
      <MessagesPerWeekdayChart :messagesPerWeekday="statistics.messages_per_weekday" />
      <MessagesByHourChart :messagesByHour="statistics.messages_per_hour" />
      <MessagesByMonthChart :messagesByMonth="statistics.messages_per_month" />
      <FirstMessagesChart :firstMessageCount="statistics.first_message_count" />

      <h2 style="margin-top: 4vw;">Laugh Expressions Counter:</h2>
      <p>{{ statistics.laugh_count }}</p>
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
import MessagesPerDayChart from './MessagesPerDayChart.vue';
import MessagesPerWeekChart from './MessagesPerWeekChart.vue';
import MessagesPerWeekdayChart from './MessagesPerWeekdayChart.vue';
import MessagesByHourChart from './MessagesByHourChart.vue';
import MessagesByMonthChart from './MessagesByMonthChart.vue';
import FirstMessagesChart from './FirstMessagesChart.vue';

export default {
  components: {
    TotalMessagesRateChart,
    CommonWordsList,
    CommonWordsChart,
    MessagesPerDayChart,
    MessagesPerWeekChart,
    MessagesPerWeekdayChart,
    MessagesByHourChart,
    MessagesByMonthChart,
    FirstMessagesChart,
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
    console.log("Statistics in created:", this.statistics);
  },
  data() {
    return {
      statistics: {}
    };
  },
  computed: {
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
    }
  },
  methods: {
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      return `${minutes}m ${remainingSeconds}s`;
    }
  }
};
</script>

<style>
</style>
