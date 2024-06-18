<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded w-full max-w-md">
      <h1 class="text-4xl font-bold mb-5 text-center">Upload Chat JSON</h1>
      <h3 class="text-lg font-base mb-5 text-center">Supports Telegram chats <br> To export chat as a JSON in Telegram Desktop, got to:</h3>
      <p class="font-light mb-5">Chat -> 3 dots -> Export chat history -> Untick all boxes and select Format: JSON</p>
      <input 
        type="file" 
        @change="handleFileUpload" 
        class="block w-full text-sm text-gray-900 cursor-pointer bg-gray-50"
      />
      <button 
        @click="uploadFile" 
        :disabled="isLoading" 
        class="mt-5 w-full bg-gray-400 text-white py-2 px-4 hover:bg-gray-600 disabled:opacity-50"
      >
        Upload
      </button>
      <div v-if="isLoading" class="mt-5 text-black text-center">
        Analyzing...
        <p class="font-light text-sm">This might take some time for large chats</p>
      </div>
      <div v-if="error" class="mt-5 text-red-500 text-center">
        <p>{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      file: null,
      error: null,
      isLoading: false,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      if (!this.file) {
        this.error = "No file selected";
        return;
      }
      this.error = null;
      this.isLoading = true;
      let formData = new FormData();
      formData.append('file', this.file);
      try {
        const response = await axios.post('https://chat-parser-279838eb8969.herokuapp.com/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.$router.push({ name: 'Statistics', query: { statistics: JSON.stringify(response.data) } });
      } catch (error) {
        this.error = 'Error uploading file: ' + (error.response ? error.response.data.error : error.message);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  font-family: 'JetBrains Mono', monospace;
  background-color: #f7fafc;
}
</style>
