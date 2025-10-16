<script setup>
defineProps(['comment'])
</script>

<template>
  <div class="comment">
    <p>{{ comment.user_name }} - {{ comment.email }} - {{ comment.created_at }}</p>
    <div v-html="comment.text"></div>
    <a v-if="comment.image" :href="comment.image" data-lightbox="image">View Image</a>
    <a v-if="comment.file" :href="comment.file">Download File</a>
    <CommentItem v-for="child in comment.children" :key="child.id" :comment="child" />
  </div>
</template>