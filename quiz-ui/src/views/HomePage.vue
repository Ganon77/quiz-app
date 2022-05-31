<style>
@import '../assets/css/home.css';
</style>

<template>
  <div class="grand-container">
    <div class="title">
      <h1>Monkey Quiz</h1>
      <img src="../assets/pics/logo.png" />
    </div>

    <div class="big-container">
      <div v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date"
        v-bind:class="'n' + index + ' box'">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>

    <router-link to="/start-quiz">
      <button>
        Démarrer le quiz !
      </button>
    </router-link>


  </div>

</template>

<script>

import quizApiService from "@/services/quizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    await quizApiService.getQuizInfo().then((response) => {
      this.registeredScores = response.data.scores
    })
  }
};
</script>