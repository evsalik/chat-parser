<template>
  <div class="statistics-container mx-auto p-5">
    <h1 class="text-2xl font-bold mb-5">Chat Statistics</h1>
    <div v-if="statistics">
      <div class="stat-item mb-5">
        <p>Total Messages: {{ statistics.total_messages }}</p>
        <p>Average Messages per Day of chatting: {{ statistics.average_messages_per_day.toFixed(2) }}</p>
        <p>Longest Conversation: {{ statistics.longest_conversation }}</p>
      </div>

      <div class="stat-item mb-5">
        <h2 class="text-xl font-medium mb-2">Percentage Rate (Largest First):</h2>
        <ul>
          <li v-for="(percentage, user) in sortedUserPercentages" :key="user">
            {{ user }} - {{ percentage.toFixed(2) }}% ({{ statistics.user_message_counts[user] }} messages)
          </li>
        </ul>
      </div>

      <div class="stat-item mb-5">
        <h2 class="text-xl font-medium mb-2">Average Response Times (Quickest First):</h2>
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
        <h2 class="text-xl font-medium mb-2">Suggested New Swear Words:</h2>
        <ul>
          <li v-for="(swear, index) in statistics.suggested_swears" :key="index">
            {{ swear }}
          </li>
        </ul>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="commonWordsListHeader" @click="toggleVisibility('commonWordsList')" class="text-xl font-medium cursor-pointer mb-2">Common Words List</h2>
        <div v-if="isVisible('commonWordsList')" class="transition-element">
          <CommonWordsList :commonWords="statistics.word_frequencies" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="totalMessagesRateChartHeader" @click="toggleVisibility('totalMessagesRateChart')" class="text-xl font-medium cursor-pointer mb-2">User Message Count Chart</h2>
        <div v-if="isVisible('totalMessagesRateChart')" class="transition-element">
          <TotalMessagesRateChart :userMessageCounts="statistics.user_message_counts" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="commonWordsChartHeader" @click="toggleVisibility('commonWordsChart')" class="text-xl font-medium cursor-pointer mb-2">Common Words Chart</h2>
        <div v-if="isVisible('commonWordsChart')" class="transition-element">
          <CommonWordsChart :commonWords="statistics.word_frequencies" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesPerDayChartHeader" @click="toggleVisibility('messagesPerDayChart')" class="text-xl font-medium cursor-pointer mb-2">Messages Per Day Chart</h2>
        <div v-if="isVisible('messagesPerDayChart')" class="transition-element">
          <MessagesPerDayChart :messagesPerDay="statistics.messages_per_day" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesPerUserPerDayChartHeader" @click="toggleVisibility('messagesPerUserPerDayChart')" class="text-xl font-medium cursor-pointer mb-2">Messages Per User Per Day Chart</h2>
        <div v-if="isVisible('messagesPerUserPerDayChart')" class="transition-element">
          <MessagesPerUserPerDayChart :statistics="statistics" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesPerWeekChartHeader" @click="toggleVisibility('messagesPerWeekChart')" class="text-xl font-medium cursor-pointer mb-2">Messages Per Week Chart</h2>
        <div v-if="isVisible('messagesPerWeekChart')" class="transition-element">
          <MessagesPerWeekChart :messagesPerWeek="statistics.messages_per_week" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesPerWeekdayChartHeader" @click="toggleVisibility('messagesPerWeekdayChart')" class="text-xl font-medium cursor-pointer mb-2">Messages Per Weekday Chart</h2>
        <div v-if="isVisible('messagesPerWeekdayChart')" class="transition-element">
          <MessagesPerWeekdayChart :messagesPerWeekday="statistics.messages_per_weekday" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesByHourChartHeader" @click="toggleVisibility('messagesByHourChart')" class="text-xl font-medium cursor-pointer mb-2">Messages By Hour Chart</h2>
        <div v-if="isVisible('messagesByHourChart')" class="transition-element">
          <MessagesByHourChart :messagesByHour="statistics.messages_per_hour" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messagesByMonthChartHeader" @click="toggleVisibility('messagesByMonthChart')" class="text-xl font-medium cursor-pointer mb-2">Messages By Month Chart</h2>
        <div v-if="isVisible('messagesByMonthChart')" class="transition-element">
          <MessagesByMonthChart :messagesByMonth="statistics.messages_per_month" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="firstMessagesChartHeader" @click="toggleVisibility('firstMessagesChart')" class="text-xl font-medium cursor-pointer mb-2">First Messages Chart</h2>
        <div v-if="isVisible('firstMessagesChart')" class="transition-element">
          <FirstMessagesChart :firstMessageCount="statistics.first_message_count" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messageLengthDistributionChartHeader" @click="toggleVisibility('messageLengthDistributionChart')" class="text-xl font-medium cursor-pointer mb-2">Message Length Distribution Chart</h2>
        <div v-if="isVisible('messageLengthDistributionChart')" class="transition-element">
          <MessageLengthDistributionChart :statistics="statistics" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="stickerEmojiChartHeader" @click="toggleVisibility('stickerEmojiChart')" class="text-xl font-medium cursor-pointer mb-2">Sticker Emoji Chart</h2>
        <div v-if="isVisible('stickerEmojiChart')" class="transition-element">
          <StickerEmojiChart :stickerEmojiCounts="statistics.sticker_emoji_counts" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="voiceMessageChartHeader" @click="toggleVisibility('voiceMessageChart')" class="text-xl font-medium cursor-pointer mb-2">Voice Message Chart</h2>
        <div v-if="isVisible('voiceMessageChart')" class="transition-element">
          <VoiceMessageChart :voiceMessageCounts="statistics.voice_message_counts" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="videoMessageChartHeader" @click="toggleVisibility('videoMessageChart')" class="text-xl font-medium cursor-pointer mb-2">Video Message Chart</h2>
        <div v-if="isVisible('videoMessageChart')" class="transition-element">
          <VideoMessageChart :videoMessageCounts="statistics.video_message_counts" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="messageLengthBoxPlotHeader" @click="toggleVisibility('messageLengthBoxPlot')" class="text-xl font-medium cursor-pointer mb-2">Message Length Box Plot</h2>
        <div v-if="isVisible('messageLengthBoxPlot')" class="transition-element">
          <MessageLengthBoxPlot :userMessageLengths="statistics.user_message_lengths" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="timeBetweenMessagesChartHeader" @click="toggleVisibility('timeBetweenMessagesChart')" class="text-xl font-medium cursor-pointer mb-2">Time Between Messages Chart</h2>
        <div v-if="isVisible('timeBetweenMessagesChart')" class="transition-element">
          <TimeBetweenMessagesChart :timeDifferences="statistics.time_differences" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="conversationCountChartHeader" @click="toggleVisibility('conversationCountChart')" class="text-xl font-medium cursor-pointer mb-2">Conversation Count Chart</h2>
        <div v-if="isVisible('conversationCountChart')" class="transition-element">
          <ConversationCountChart :conversations="statistics.conversation_details" />
        </div>
      </div>

      <div class="chart-container mb-5">
        <h2 ref="conversationLengthsChartHeader" @click="toggleVisibility('conversationLengthsChart')" class="text-xl font-medium cursor-pointer mb-2">Conversation Lengths Chart</h2>
        <div v-if="isVisible('conversationLengthsChart')" class="transition-element">
          <ConversationLengthsChart :sortedConversationLengths="statistics.sorted_conversation_lengths" />
        </div>
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
import ConversationCountChart from './ConversationCountChart.vue';
import ConversationLengthsChart from './ConversationLengthsChart.vue';

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
      statistics: {},
      visibility: {
        commonWordsList: false,
        totalMessagesRateChart: false,
        commonWordsChart: false,
        messagesPerDayChart: false,
        messagesPerUserPerDayChart: false,
        messagesPerWeekChart: false,
        messagesPerWeekdayChart: false,
        messagesByHourChart: false,
        messagesByMonthChart: false,
        firstMessagesChart: false,
        messageLengthDistributionChart: false,
        stickerEmojiChart: false,
        voiceMessageChart: false,
        videoMessageChart: false,
        messageLengthBoxPlot: false,
        timeBetweenMessagesChart: false,
        conversationCountChart: false,
        conversationLengthsChart: false,
      }
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
    },
    toggleVisibility(key) {
      this.visibility[key] = !this.visibility[key];
      const header = this.$refs[key + 'Header'];
      if (this.visibility[key]) {
        header.classList.add('bold');
      } else {
        header.classList.remove('bold');
      }
    },
    isVisible(key) {
      return this.visibility[key];
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
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  font-weight: 300;
  cursor: pointer;
  user-select: none;
}

h2.bold {
  font-weight: 900;
}
</style>
