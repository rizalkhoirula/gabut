<template>
  <div v-if="hasResults || error" class="results-container">
    <div v-if="error" class="error-box">
      <h3>Error</h3>
      <p>{{ error }}</p>
    </div>
    <div v-else-if="foodName">
      <h2>Recognition Results</h2>

      <div class="result-item">
        <strong>Detected Food:</strong> <span>{{ foodName }}</span>
      </div>

      <div v-if="yoloMessage" class="result-item yolo-message">
        <small>{{ yoloMessage }}</small>
      </div>

      <div v-if="recipe && recipe !== '' && !recipe.toLowerCase().includes('not available') && !recipe.toLowerCase().includes('error')" class="result-item recipe-section">
        <h3>Recipe for {{ foodName }}</h3>
        <h4>Ingredients:</h4>
        <pre>{{ formatIngredients(recipe) }}</pre>
      </div>
      <div v-else-if="recipe" class="result-item recipe-section">
         <p><em>Recipe information: {{ recipe }}</em></p>
      </div>


      <div v-if="instructions && instructions !== '' && !instructions.toLowerCase().includes('not available') && !instructions.toLowerCase().includes('error')" class="result-item instructions-section">
        <h4>Cooking Instructions:</h4>
        <pre>{{ formatInstructions(instructions) }}</pre>
      </div>
       <div v-else-if="instructions" class="result-item instructions-section">
         <p><em>Cooking instructions: {{ instructions }}</em></p>
      </div>

    </div>
    <div v-else-if="!isLoading && hasAttempted"> <!-- if no food name but not loading and an attempt was made -->
        <p>No food item was recognized in the image, or recipe details could not be retrieved.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  foodName: String,
  yoloMessage: String,
  recipe: String,
  instructions: String,
  error: String,
  isLoading: Boolean,
  hasAttempted: Boolean // New prop to know if an upload attempt was made
});

const hasResults = computed(() => {
  return props.foodName || props.yoloMessage || props.recipe || props.instructions;
});

// Basic formatting, LLM output can be complex
const formatIngredients = (text) => {
  if (!text) return '';
  return text.replace(/^Ingredients:/i, '').trim().split('\n').map(line => line.trim()).join('\n');
};

const formatInstructions = (text) => {
  if (!text) return '';
  return text.replace(/^Instructions:/i, '').trim().split('\n').map(line => line.trim()).join('\n');
};

</script>

<style scoped>
.results-container {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.result-item {
  margin-bottom: 15px;
}
.result-item strong {
  color: #333;
}
.yolo-message {
  font-style: italic;
  color: #555;
  font-size: 0.9em;
}
.recipe-section h3, .instructions-section h3 {
  color: #007bff;
  margin-bottom: 10px;
}
.recipe-section h4, .instructions-section h4 {
  color: #333;
  margin-top: 10px;
  margin-bottom: 5px;
}
pre {
  white-space: pre-wrap; /* Allows text to wrap */
  word-wrap: break-word; /* Breaks long words */
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #eee;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.95em;
  line-height: 1.6;
}
.error-box {
  padding: 15px;
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
  color: #c62828;
  border-radius: 4px;
}
.error-box h3 {
  margin-top: 0;
  color: #c62828;
}
</style>
