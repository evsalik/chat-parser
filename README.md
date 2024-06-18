# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended Setup

- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar) and disable Vetur

- Use [vue-tsc](https://github.com/vuejs/language-tools/tree/master/packages/tsc) for performing the same type checking from the command line, or for generating d.ts files for SFCs.



```
parser-v0
├─ .gitignore
├─ README.md
├─ backend
│  ├─ app.py
│  ├─ package.json
│  └─ requirements.txt
├─ frontend
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ postcss.config.js
│  ├─ public
│  │  └─ vite.svg
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  │  ├─ cp.svg
│  │  │  └─ tailwind.css
│  │  ├─ components
│  │  │  ├─ ChartSelection.vue
│  │  │  ├─ StatItems.vue
│  │  │  ├─ Statistics.vue
│  │  │  ├─ Upload.vue
│  │  │  └─ charts
│  │  │     ├─ CommonWordsChart.vue
│  │  │     ├─ CommonWordsList.vue
│  │  │     ├─ ConversationCountChart.vue
│  │  │     ├─ ConversationLengthsChart.vue
│  │  │     ├─ FirstMessagesChart.vue
│  │  │     ├─ MessageLengthBoxPlot.vue
│  │  │     ├─ MessageLengthDistributionChart.vue
│  │  │     ├─ MessagesByHourChart.vue
│  │  │     ├─ MessagesByMonthChart.vue
│  │  │     ├─ MessagesPerDayChart.vue
│  │  │     ├─ MessagesPerUserPerDayChart.vue
│  │  │     ├─ MessagesPerWeekChart.vue
│  │  │     ├─ MessagesPerWeekdayChart.vue
│  │  │     ├─ StickerEmojiChart.vue
│  │  │     ├─ TimeBetweenMessagesChart.vue
│  │  │     ├─ TotalMessagesRateChart.vue
│  │  │     ├─ VideoMessageChart.vue
│  │  │     └─ VoiceMessageChart.vue
│  │  ├─ main.ts
│  │  ├─ style.css
│  │  └─ vite-env.d.ts
│  ├─ tailwind.config.js
│  ├─ tsconfig.json
│  ├─ tsconfig.node.json
│  └─ vite.config.ts
├─ package-lock.json
├─ package.json
└─ yarn.lock

```