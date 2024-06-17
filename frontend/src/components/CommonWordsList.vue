<template>
  <div class="list-container">
    <ol>
      <li v-for="(word, index) in commonWords" :key="index">{{ word[0] }} - {{ word[1] }}</li>
    </ol>
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
  height: 400px;
  overflow-y: scroll;
  border: 1px solid #ddd;
  padding: 10px;
}
</style>
