<template>
  <div>
    <h1>Upload Chat JSON</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile">Upload</button>
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
      let formData = new FormData();
      formData.append('file', this.file);
      try {
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // Pass data as a query parameter
        this.$router.push({ name: 'Statistics', query: { statistics: JSON.stringify(response.data) } });
      } catch (error) {
        this.error = 'Error uploading file: ' + (error.response ? error.response.data.error : error.message);
      }
    },
  },
};
</script>

<style>
/* Add your styles here */
</style>
