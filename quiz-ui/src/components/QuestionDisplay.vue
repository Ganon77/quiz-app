<style>
@import '../assets/css/questionDisplay.css';
</style>

<template>
  <div v-if="question" class="answer-container">
    <h2>{{question.text}}</h2>
    <img class="pic" v-if="question.image" :src="question.image" />

    <div class="answer-wrapper">
      <template v-if="isAdmin" v-for="answer in question.possibleAnswers">
        <div v-if="answer.isCorrect"  class="goodAnswer">
          <div class="answerText">{{answer.text}}</div>
        </div>
        <div v-else class="wrongAnwser">
          <div class="answerText">{{answer.text}}</div>
        </div>
      </template>
      <template v-else>
        <div v-for="(answer, index) in question.possibleAnswers" class="answer" @click="$emit('answer-selected', index+1)">
          <div class="answerText">{{answer.text}}</div>
        </div>
      </template>      
    </div>

    <div v-if="isAdmin" class="button-wrapper">
      <button class="button" @click="goToEdit">Modifier</button>
      <button class="button">Supprimer</button>
    </div>
    
  </div>  
</template>

<script>
export default {
  props: {
    question: {
      type: Object
    },
    isAdmin: {
      type: Boolean
    }
  },
  methods: {
    goToEdit(){
     this.$router.push(`/edit-question/${this.question.position}`);
    }
  }
}
</script>
