<template>
  <div class="chart-selection mb-5">
    <h2 v-for="chart in charts" :key="chart.name" @click="selectChart(chart.name)" :class="{'bold': selectedChart === chart.name}" class="text-lg font-light cursor-pointer mb-2">
      {{ chart.displayName }}
    </h2>
  </div>
</template>

<script>
export default {
  name: 'ChartSelection',
  props: {
    selectedChart: {
      type: String,
      required: true,
    },
  },
  emits: ['chartSelected'],
  data() {
    return {
      charts: [
        { name: 'CommonWordsList', displayName: 'Common Words List' },
        { name: 'TotalMessagesRateChart', displayName: 'User Message Count Chart' },
        { name: 'CommonWordsChart', displayName: 'Common Words Chart' },
        { name: 'MessagesPerDayChart', displayName: 'Messages Per Day Chart' },
        { name: 'MessagesPerUserPerDayChart', displayName: 'Messages Per User Per Day Chart' },
        { name: 'MessagesPerWeekChart', displayName: 'Messages Per Week Chart' },
        { name: 'MessagesPerWeekdayChart', displayName: 'Messages Per Weekday Chart' },
        { name: 'MessagesByHourChart', displayName: 'Messages By Hour Chart' },
        { name: 'MessagesByMonthChart', displayName: 'Messages By Month Chart' },
        { name: 'FirstMessagesChart', displayName: 'First Messages Chart' },
        { name: 'MessageLengthDistributionChart', displayName: 'Message Length Distribution Chart' },
        { name: 'StickerEmojiChart', displayName: 'Sticker Emoji Chart' },
        { name: 'VoiceMessageChart', displayName: 'Voice Message Chart' },
        { name: 'VideoMessageChart', displayName: 'Video Message Chart' },
        { name: 'MessageLengthBoxPlot', displayName: 'Message Length Box Plot' },
        { name: 'TimeBetweenMessagesChart', displayName: 'Time Between Messages Chart' },
        { name: 'ConversationCountChart', displayName: 'Conversation Count Chart' },
        { name: 'ConversationLengthsChart', displayName: 'Conversation Lengths Chart' },
      ],
    };
  },
  methods: {
    selectChart(chartName) {
      this.$emit('chartSelected', chartName);
    },
  },
};
</script>

<style scoped>
h2 {
  font-weight: 100;
  cursor: pointer;
  user-select: none;
}

h2.bold {
  font-weight: 700;
}
</style>
