<template>
  <div class="uploader-container">
    <h2>Upload Food Image</h2>
    <input type="file" @change="handleFileSelect" accept="image/png, image/jpeg, image/jpg" />
    <button @click="uploadImage" :disabled="!selectedFile || isLoading">
      {{ isLoading ? "Processing..." : "Recognize Food" }}
    </button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="isLoading">Please wait, the model is processing the image...</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedFile = ref(null);
const isLoading = ref(false);
const errorMessage = ref('');

const emit = defineEmits(['upload-success', 'upload-error', 'processing']);

const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0];
  errorMessage.value = ''; // Clear previous errors
};

const uploadImage = async () => {
  if (!selectedFile.value) {
    errorMessage.value = 'Please select an image file first.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  emit('processing'); // Notify parent that processing has started

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  try {
    // Assuming backend is running on localhost:5000
    // In a real app, this URL should be configurable
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle HTTP errors (e.g., 400, 404, 500)
      const errorMsg = data.error || `Server error: ${response.status}`;
      throw new Error(errorMsg);
    }

    // Check if the response contains food_name, otherwise it's an error from the backend logic
    // (e.g. "No food item detected") even if HTTP status is 200
    if (data.food_name) {
        emit('upload-success', data);
    } else if (data.error) {
        // This handles cases where the server responds 200 OK but detection failed
        throw new Error(data.error);
    } else {
        // Fallback for unexpected response structure
        throw new Error('Unexpected response structure from server.');
    }

  } catch (error) {
    console.error('Upload error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred during upload.';
    emit('upload-error', { error: errorMessage.value });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.uploader-container {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px dashed #007bff;
  border-radius: 8px;
  text-align: center;
  background-color: #f8f9fa;
}
input[type="file"] {
  margin-bottom: 15px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background-color: #0056b3;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
