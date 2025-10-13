<script setup>
defineProps(['text'])
defineEmits(['close'])
</script>

<template>
  <div class="modal">
    <div v-html="text"></div>
    <button @click="$emit('close')">Close</button>
  </div>
</template>

<style>
.modal { position: fixed; top: 50%; left: 50%; background: white; padding: 20px; }
</style>