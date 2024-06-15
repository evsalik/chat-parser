<template>
  <div class="statistics-container">
    <h1>Chat Statistics</h1>
    <div v-if="statistics">
      <div class="stat-item">
        <p>Total Messages: {{ statistics.total_messages }}</p>
        <p>Average Messages per Day: {{ statistics.average_messages_per_day.toFixed(2) }}</p>
      </div>

      <div class="stat-item">
        <h2>Percentage Rate (Largest First):</h2>
        <ul>
          <li v-for="(percentage, user) in sortedUserPercentages" :key="user">
            {{ user }} - {{ percentage.toFixed(2) }}% ({{ statistics.user_message_counts[user] }} messages)
          </li>
        </ul>
      </div>

      <div class="stat-item">
        <h2>Average Response Times (Quickest First):</h2>
        <ul>
          <li v-for="(time, user) in sortedAverageResponseTimes" :key="user">
            {{ user }} - {{ formatTime(time) }}
          </li>
        </ul>
      </div>

      <div class="stat-item">
        <h2>Top 10 Most Active Days:</h2>
      <ul>
        <li v-for="(day, index) in statistics.top_10_days" :key="index">
          {{ day[0] }} - {{ day[1] }} messages
        </li>
      </ul>
      </div>

      <div class="stat-item">
        <h2>Laugh Expressions Counter:</h2>
        <p>{{ statistics.laugh_count }}</p>
      </div>

      <div class="stat-item">
        <h2>Swear Words Statistics:</h2>
        <p>Total Swears: {{ statistics.swear_count }}</p>
        <p>Swear Rate: {{ statistics.swear_rate.toFixed(2) }}%</p>
        <ul>
          <li v-for="([count, swears], index) in sortedGroupedSwearFrequencies" :key="index">
            {{ count }}: {{ swears.join(', ') }}
          </li>
        </ul>
      </div>

      <div class="stat-item" style="margin-top: -20px;">
        <h2>Suggested New Swear Words:</h2>
        <ul>
          <li v-for="(swear, index) in statistics.suggested_swears" :key="index">
            {{ swear }}
          </li>
        </ul>
      </div>

      <div class="chart-container">
        <CommonWordsList :commonWords="statistics.word_frequencies" />
      </div>

      <div class="chart-container">
        <TotalMessagesRateChart :userMessageCounts="statistics.user_message_counts" />
      </div>
      <div class="chart-container">
        <CommonWordsChart :commonWords="statistics.word_frequencies" />
      </div>
      <div class="chart-container">
        <MessagesPerDayChart :messagesPerDay="statistics.messages_per_day" />
      </div>
      <div class="chart-container" style="margin-top: 60px;">
        <MessagesPerUserPerDayChart :statistics="statistics" />
      </div>
      <div class="chart-container">
        <MessagesPerWeekChart :messagesPerWeek="statistics.messages_per_week" />
      </div>
      <div class="chart-container">
        <MessagesPerWeekdayChart :messagesPerWeekday="statistics.messages_per_weekday" />
      </div>
      <div class="chart-container">
        <MessagesByHourChart :messagesByHour="statistics.messages_per_hour" />
      </div>
      <div class="chart-container">
        <MessagesByMonthChart :messagesByMonth="statistics.messages_per_month" />
      </div>
      <div class="chart-container" style="margin-top: 60px;">
        <FirstMessagesChart :firstMessageCount="statistics.first_message_count" />
      </div>
      <div class="chart-container">
        <MessageLengthDistributionChart :statistics="statistics" />
      </div>
      <div class="chart-container">
        <StickerEmojiChart :stickerEmojiCounts="statistics.sticker_emoji_counts" />
      </div>
      <div class="chart-container">
        <VoiceMessageChart :voiceMessageCounts="statistics.voice_message_counts" />
      </div>
      <div class="chart-container">
        <VideoMessageChart :videoMessageCounts="statistics.video_message_counts" />
      </div>
      <div class="chart-container">
        <MessageLengthBoxPlot :userMessageLengths="statistics.user_message_lengths" />
      </div>
      <div>
        <TimeBetweenMessagesChart :timeDifferences="statistics.time_differences" />
      </div>
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
import MessageLengthDistributionChart from './MessageLengthDistributionChart.vue';
import MessagesPerUserPerDayChart from './MessagesPerUserPerDayChart.vue';
import StickerEmojiChart from './StickerEmojiChart.vue';
import VoiceMessageChart from './VoiceMessageChart.vue';
import VideoMessageChart from './VideoMessageChart.vue';
import MessageLengthBoxPlot from './MessageLengthBoxPlot.vue';
import TimeBetweenMessagesChart from './TimeBetweenMessagesChart.vue';

export default {
  components: {
    TimeBetweenMessagesChart,
    MessageLengthBoxPlot,
    VideoMessageChart,
    VoiceMessageChart,
    StickerEmojiChart,
    TotalMessagesRateChart,
    CommonWordsList,
    CommonWordsChart,
    MessagesPerDayChart,
    MessagesPerWeekChart,
    MessagesPerWeekdayChart,
    MessagesByHourChart,
    MessagesByMonthChart,
    FirstMessagesChart,
    MessageLengthDistributionChart,
    MessagesPerUserPerDayChart
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
.statistics-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-item {
  margin-bottom: 40px;
}

.chart-container {
  margin-bottom: 40px;
}
</style>
