<style>
</style>


<template>
    <div>
        <h1>Votre Score : {{score}}</h1>

        <div class="start-quiz">
          <button @click="goBackHome" type="submit">Retour</button>
        </div>
    </div>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";

export default {
  name: "Score",
  data() {
    return {
        playerName: "",
        score: 0,
    };
  },
  async created() {
      this.playerName = participationStorageService.getPlayerName();
      this.score = participationStorageService.getParticipationScore();
  },
  methods: {
    goBackHome() {
      this.$router.push('/');
    },
  },
};
</script>