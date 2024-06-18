<template>
  <div class="statistics-container mx-auto p-3">
    <h1 class="text-4xl font-bold mb-5">Chat Statistics</h1>
    <div v-if="Object.keys(statistics).length > 0" class="flex">
      <!-- Sidebar for Chart Selection -->
      <div class="sidebar w-1/5 pr-5 pt-5">
        <ChartSelection :selectedChart="currentChartComponent" @chartSelected="showChart" />
      </div>

      <!-- Main Content Area -->
      <div class="main-content w-1/5 pt-5">
        <!-- Stat Items -->
        <StatItems :statistics="statistics" />
      </div>

      <!-- Chart Display Area -->
      <div class="chart-display w-3/5 pt-5 ml-10">
        <h2 class="text-2xl font-semibold mb-5" v-if="currentChartDisplayName">{{ currentChartDisplayName }}</h2>
        <component :is="currentChartComponent" v-bind="currentChartProps" />
      </div>
    </div>
    <div v-else>
      <p>Loading statistics...</p>
    </div>
  </div>
</template>

<script>
import TotalMessagesRateChart from './charts/TotalMessagesRateChart.vue';
import CommonWordsList from './charts/CommonWordsList.vue';
import CommonWordsChart from './charts/CommonWordsChart.vue';
import MessagesPerDayChart from './charts/MessagesPerDayChart.vue';
import MessagesPerWeekChart from './charts/MessagesPerWeekChart.vue';
import MessagesPerWeekdayChart from './charts/MessagesPerWeekdayChart.vue';
import MessagesByHourChart from './charts/MessagesByHourChart.vue';
import MessagesByMonthChart from './charts/MessagesByMonthChart.vue';
import FirstMessagesChart from './charts/FirstMessagesChart.vue';
import MessageLengthDistributionChart from './charts/MessageLengthDistributionChart.vue';
import MessagesPerUserPerDayChart from './charts/MessagesPerUserPerDayChart.vue';
import StickerEmojiChart from './charts/StickerEmojiChart.vue';
import VoiceMessageChart from './charts/VoiceMessageChart.vue';
import VideoMessageChart from './charts/VideoMessageChart.vue';
import MessageLengthBoxPlot from './charts/MessageLengthBoxPlot.vue';
import TimeBetweenMessagesChart from './charts/TimeBetweenMessagesChart.vue';
import ConversationCountChart from './charts/ConversationCountChart.vue';
import ConversationLengthsChart from './charts/ConversationLengthsChart.vue';
import ChartSelection from './ChartSelection.vue';
import StatItems from './StatItems.vue';

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
    MessagesPerUserPerDayChart,
    ConversationCountChart,
    ConversationLengthsChart,
    ChartSelection,
    StatItems,
  },
  data() {
    return {
      statistics: {},
      currentChartComponent: null,
      currentChartProps: {},
      currentChartDisplayName: ''
    };
  },
  created() {
    const stats = this.$route.query.statistics;
    if (stats) {
      this.statistics = JSON.parse(stats);
    }
    console.log("Statistics in created:", this.statistics);
  },
  methods: {
    showChart(chartName) {
      const chart = this.getChartInfo(chartName);
      this.currentChartComponent = chart.name;
      this.currentChartProps = chart.props;
      this.currentChartDisplayName = chart.displayName;
    },
    getChartInfo(chartName) {
      const charts = [
        { name: 'TotalMessagesRateChart', displayName: 'User Message Count Chart', props: { userMessageCounts: this.statistics.user_message_counts } },
        { name: 'CommonWordsList', displayName: 'Common Words List', props: { commonWords: this.statistics.word_frequencies } },
        { name: 'CommonWordsChart', displayName: 'Common Words Chart', props: { commonWords: this.statistics.word_frequencies } },
        { name: 'MessagesPerDayChart', displayName: 'Messages Per Day Chart', props: { messagesPerDay: this.statistics.messages_per_day } },
        { name: 'MessagesPerUserPerDayChart', displayName: 'Messages Per User Per Day Chart', props: { statistics: this.statistics } },
        { name: 'MessagesPerWeekChart', displayName: 'Messages Per Week Chart', props: { messagesPerWeek: this.statistics.messages_per_week } },
        { name: 'MessagesPerWeekdayChart', displayName: 'Messages Per Weekday Chart', props: { messagesPerWeekday: this.statistics.messages_per_weekday } },
        { name: 'MessagesByHourChart', displayName: 'Messages By Hour Chart', props: { messagesByHour: this.statistics.messages_per_hour } },
        { name: 'MessagesByMonthChart', displayName: 'Messages By Month Chart', props: { messagesByMonth: this.statistics.messages_per_month } },
        { name: 'FirstMessagesChart', displayName: 'First Messages Chart', props: { firstMessageCount: this.statistics.first_message_count } },
        { name: 'MessageLengthDistributionChart', displayName: 'Message Length Distribution Chart', props: { statistics: this.statistics } },
        { name: 'StickerEmojiChart', displayName: 'Sticker Emoji Chart', props: { stickerEmojiCounts: this.statistics.sticker_emoji_counts } },
        { name: 'VoiceMessageChart', displayName: 'Voice Message Chart', props: { voiceMessageCounts: this.statistics.voice_message_counts } },
        { name: 'VideoMessageChart', displayName: 'Video Message Chart', props: { videoMessageCounts: this.statistics.video_message_counts } },
        { name: 'MessageLengthBoxPlot', displayName: 'Message Length Box Plot', props: { userMessageLengths: this.statistics.user_message_lengths } },
        { name: 'TimeBetweenMessagesChart', displayName: 'Time Between Messages Chart', props: { timeDifferences: this.statistics.time_differences } },
        { name: 'ConversationCountChart', displayName: 'Conversation Count Chart', props: { conversations: this.statistics.conversation_details } },
        { name: 'ConversationLengthsChart', displayName: 'Conversation Lengths Chart', props: { sortedConversationLengths: this.statistics.sorted_conversation_lengths } },
      ];

      return charts.find(chart => chart.name === chartName);
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap');

body {
  font-family: 'JetBrains Mono', monospace;
}

.statistics-container {
  margin: 0 auto;
}

.sidebar {
  border-right: 1px solid #ccc;
}

.main-content {
  padding-left: 20px;
}

.chart-display {
  margin-top: 20px;
  height: 80vh;
  max-height: 80vh;
  overflow-y: auto;
}
</style>
