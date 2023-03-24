<style>
@import '../assets/css/home.css';
</style>

<template>
  <div class="grand-container">
    <div class="title">
      <h1>Monkey Quiz</h1>
      <img src="../assets/pics/logo.png" />
    </div>

    <div class="home-big-container" v-if="registeredScores.length >= 1">
      <template v-for="index in registeredScores.length">
        <div v-if="index <= 3"  v-bind:class="'n' + index">
          {{ registeredScores[index-1].playerName }} - {{ registeredScores[index-1].score }}
          <img class="picto" src="../assets/pics/banana_3.png" v-if="index == 1" />
          <img class="picto" src="../assets/pics/banana_2.png" v-if="index == 2" />
          <img class="picto" src="../assets/pics/banana_1.png" v-if="index == 3" />
        </div>
        <div v-else class="box">
          {{ registeredScores[index-1].playerName }} - {{ registeredScores[index-1].score }}
        </div>
      </template>
    </div>

    <router-link to="/start-quiz">
      <button>
        Démarrer le quiz !
      </button>
    </router-link>
  </div>

</template>

<script>

import quizApiService from "@/services/QuizApiService";

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

    console.log(this.registeredScores[0].playerName)
  }
};
</script>