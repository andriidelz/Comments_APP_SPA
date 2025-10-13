<script setup>
defineEmits(['insert'])
</script>

<template>
  <button @click="$emit('insert', 'i')">[i]</button>
  <button @click="$emit('insert', 'strong')">[strong]</button>
  <button @click="$emit('insert', 'code')">[code]</button>
  <button @click="$emit('insert', { tag: 'a', attrs: { href: '', title: '' } })">[a]</button>
</template>