<script setup>
import { defineProps } from 'vue'
defineProps({
  comment: Object
})
</script>

<template>
  <div class="comment">
    <p>
      <strong>{{ comment.user_name }}</strong> - {{ comment.email }} - {{ new Date(comment.created_at).toLocaleString() }}
    </p>

    <div v-html="comment.text"></div>

    <a 
      v-if="comment.image" 
      :href="comment.image" 
      data-lightbox="gallery" 
      :data-title="`${comment.user_name} - ${new Date(comment.created_at).toLocaleString()}`"
    >
      <img :src="comment.image" alt="Comment Image" class="thumbnail">
    </a>

    <a v-if="comment.file" :href="comment.file" download>Download File</a>

    <div class="child-comments" v-if="comment.children && comment.children.length">
      <CommentItem 
        v-for="child in comment.children" 
        :key="child.id" 
        :comment="child" 
      />
    </div>
  </div>
</template>

<style scoped>
.comment {
  border: 1px solid #ccc;
  margin: 10px;
  padding: 10px;
  border-radius: 5px;
}

.child-comments {
  margin-left: 20px;
  margin-top: 10px;
}

.thumbnail {
  max-width: 150px;
  max-height: 150px;
  margin-top: 5px;
  border-radius: 3px;
  cursor: pointer;
  transition: transform 0.2s;
}

.thumbnail:hover {
  transform: scale(1.05);
}
</style>

<!-- <script setup>
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
</template> -->