<template>
  <div>
    <h1>Chat Statistics</h1>
    <div v-if="statistics">
      <p>Total Messages: {{ statistics.total_messages }}</p>
      <p>Average Messages per Day: {{ statistics.average_messages_per_day.toFixed(2) }}</p>
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
      <MessagesPerDayChart :messagesPerDay="statistics.messages_per_day" />
      <MessagesPerWeekChart :messagesPerWeek="statistics.messages_per_week" />
      <MessagesPerWeekdayChart :messagesPerWeekday="statistics.messages_per_weekday" />
      <FirstMessagesChart :firstMessageCount="statistics.first_message_count" />
      <MessagesByHourChart :messagesByHour="statistics.messages_per_hour" />
      <MessagesByMonthChart :messagesByMonth="statistics.messages_per_month" />
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
import FirstMessagesChart from './FirstMessagesChart.vue';
import MessagesByHourChart from './MessagesByHourChart.vue';
import MessagesByMonthChart from './MessagesByMonthChart.vue';

export default {
  components: {
    TotalMessagesRateChart,
    CommonWordsList,
    CommonWordsChart,
    MessagesPerDayChart,
    MessagesPerWeekChart,
    MessagesPerWeekdayChart,
    FirstMessagesChart,
    MessagesByHourChart,
    MessagesByMonthChart
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
  }
};
</script>

<style>
</style>
