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
│  ├─ public
│  │  └─ vite.svg
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  ├─ components
│  │  │  ├─ CommonWordsChart.vue
│  │  │  ├─ CommonWordsList.vue
│  │  │  ├─ FirstMessagesChart.vue
│  │  │  ├─ MessageLengthDistributionChart.vue
│  │  │  ├─ MessagesByHourChart.vue
│  │  │  ├─ MessagesByMonthChart.vue
│  │  │  ├─ MessagesPerDayChart.vue
│  │  │  ├─ MessagesPerWeekChart.vue
│  │  │  ├─ MessagesPerWeekdayChart.vue
│  │  │  ├─ Statistics.vue
│  │  │  ├─ TotalMessagesRateChart.vue
│  │  │  └─ Upload.vue
│  │  ├─ main.ts
│  │  ├─ style.css
│  │  └─ vite-env.d.ts
│  ├─ tsconfig.json
│  ├─ tsconfig.node.json
│  └─ vite.config.ts
├─ package-lock.json
├─ package.json
└─ yarn.lock

```