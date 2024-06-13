<template>
  <div class="list-container">
    <h2>500 Most Common Words</h2>
    <ul>
      <li v-for="(word, index) in commonWords" :key="index">{{ word[0] }} - {{ word[1] }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'CommonWordsList',
  props: {
    commonWords: {
      type: Array,
      required: true
    }
  }
}
</script>

<style>
.list-container {
  margin-top: 4vw;
  height: 400px;
  overflow-y: scroll;
  border: 1px solid #ddd;
  padding: 10px;
}
</style>
