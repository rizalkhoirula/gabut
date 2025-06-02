<template>
  <div id="app-container">
    <h1>AI Food Recognition & Recipe Finder</h1>
    <p class="tagline">Upload an image of a food item, and let AI tell you what it is and how to cook it!</p>

    <ImageUploader
      @upload-success="handleSuccess"
      @upload-error="handleError"
      @processing="handleProcessing"
    />

    <div v-if="isAppLoading" class="app-loading">
      <p>Loading results...</p>
      <!-- You could add a spinner here -->
    </div>

    <ResultsDisplay
      :foodName="recognitionResult.foodName"
      :yoloMessage="recognitionResult.yoloMessage"
      :recipe="recognitionResult.recipe"
      :instructions="recognitionResult.instructions"
      :error="appError"
      :isLoading="isAppLoading"
      :hasAttempted="hasUploadAttempted"
    />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import ImageUploader from "./components/ImageUploader.vue";
import ResultsDisplay from "./components/ResultsDisplay.vue";

const recognitionResult = reactive({
  foodName: null,
  yoloMessage: null,
  recipe: null,
  instructions: null,
});

const appError = ref(null);
const isAppLoading = ref(false); // Indicates overall app loading state for results
const hasUploadAttempted = ref(false); // Tracks if an upload has been tried

const handleProcessing = () => {
  isAppLoading.value = true;
  hasUploadAttempted.value = true; // Mark that an attempt has been made
  appError.value = null; // Clear previous errors
  // Reset previous results
  recognitionResult.foodName = null;
  recognitionResult.yoloMessage = null;
  recognitionResult.recipe = null;
  recognitionResult.instructions = null;
};

const handleSuccess = (data) => {
  recognitionResult.foodName = data.food_name;
  recognitionResult.yoloMessage = data.yolo_message;
  recognitionResult.recipe = data.recipe;
  recognitionResult.instructions = data.instructions;
  appError.value = null;
  isAppLoading.value = false;
};

const handleError = (errorData) => {
  appError.value = errorData.error || 'An unknown error occurred.';
  recognitionResult.foodName = null;
  recognitionResult.yoloMessage = null;
  recognitionResult.recipe = null;
  recognitionResult.instructions = null;
  isAppLoading.value = false;
};

</script>

<style>
/* Global styles - can be moved to style.css if preferred */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f4f7f6;
  color: #333;
  line-height: 1.6;
}

#app-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 10px;
}

.tagline {
  text-align: center;
  color: #555;
  margin-bottom: 30px;
  font-size: 1.1em;
}

.app-loading {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
  color: #007bff;
}

/* Basic responsive touch */
@media (max-width: 768px) {
  #app-container {
    margin: 20px;
    padding: 20px;
  }
  h1 {
    font-size: 1.8em;
  }
  .tagline {
    font-size: 1em;
  }
}
</style>
