<style>
</style>


<template>
  <h1>Questions</h1>
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
  methods: {

  },
  components: {
    QuestionsManager
  },
  async created() {
    console.log(this.username);
  }

};
</script>