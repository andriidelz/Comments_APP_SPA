<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <h1>Comments App</h1>
  </header>
  <RouterView />
</template>

<style>
body { font-family: Arial, sans-serif; }
.comment { border: 1px solid #ccc; margin: 10px; padding: 10px; }
</style>