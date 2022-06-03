<style>
</style>


<template>
  <QuestionsManager></QuestionsManager>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";
import QuestionsManager from '../components/QuestionsManager.vue'
export default {
  name: "Questions",
  data() {
    return {
    };
  },
  components: {
    QuestionsManager
  },
  async created() {
  }

};
</script>