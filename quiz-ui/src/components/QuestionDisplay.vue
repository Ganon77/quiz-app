<style>
@import '../assets/css/questionDisplay.css';
</style>

<template>
  <div v-if="question" class="answer-container">
    <h2 >{{question.text}}</h2>
    <img class="pic" v-if="question.image" :src="question.image" />
    <div v-for="(answer, index) in question.possibleAnswers" class="answer" @click="$emit('answer-selected', index+1)">
      <a class="answerText">{{answer.text}}</a>
    </div>
  </div>  
</template>

<script>
export default {
  props: {
    question: {
      type: Object
    }
  }
}
</script>
