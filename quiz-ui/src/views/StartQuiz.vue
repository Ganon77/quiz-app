<style>
@import '../assets/css/quiz-start.css';
</style>


<template>
  <h1>Quiz</h1>

  <form action="Questions.vue">
    <div class="form-container">
      <div class="name-wrapper">
        <label for="name">Saississez votre nom:</label>
        <input type="text" name="name" v-model="username" />
      </div>
      <div class="start-quiz">
        <button @click="launchNewQuiz" type="submit">Commencer</button>
      </div>
    </div>
  </form>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";

export default {
  name: "StartQuiz",
  data() {
    return {
      username: ""
    };
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  },
  async created() {
  }

};
</script>