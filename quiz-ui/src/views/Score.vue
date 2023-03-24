<style>
@import '../assets/css/score.css';
</style>


<template>
    <div class="score-wrapper">
        <h1>{{playerName}} vous avez {{score}} bonnes réponses</h1>
      
        <div class="top3">
          <h2>Top 3 des meilleurs joueurs</h2>
          <template v-for="index in registeredScores.length">
            <div class="box">
              {{ registeredScores[index-1].playerName }} - {{ registeredScores[index-1].score }}
            </div>
          </template>
        </div>

        <div class="back-home">
          <button @click="goBackHome" type="submit">Retour</button>
        </div>
    </div>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";

export default {
  name: "Score",
  data() {
    return {
        playerName: "",
        score: 0,
        registeredScores: []
    };
  },
  async created() {
      this.playerName = participationStorageService.getPlayerName();
      this.score = participationStorageService.getParticipationScore();

      await quizApiService.getQuizInfo().then((response) => {
        this.registeredScores = response.data.scores
      })
  },
  methods: {
    goBackHome() {
      this.$router.push('/');
    },
  },
};
</script>