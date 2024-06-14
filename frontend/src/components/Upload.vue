<template>
  <div>
    <h1>Upload Chat JSON</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile" :disabled="isLoading">Upload</button>
    <div v-if="isLoading">Analizando...</div>
    <div v-if="error" style="color: red;">
      <p>{{ error }}</p>
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
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
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

<style>
</style>
