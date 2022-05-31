<template>
  <h1>Home page</h1>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/start-quiz">Démarrer le quiz !</router-link>
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