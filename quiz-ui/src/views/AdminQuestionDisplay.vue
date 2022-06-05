<style>
</style>

<template v-if="token != null">
  <div>
    <QuestionDisplay v-if="question" :question="question" :isAdmin="true" v-bind:is="QuestionDisplay"/>
  </div>
</template>

<script>
import QuestionDisplay from "../components/QuestionDisplay.vue"
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "AdminQuestionDisplay",
  data() {
    return {
        token: null,
        question: null
    };
  },
  components: {
    QuestionDisplay
  },
  created(){
      this.position = this.$route.params.position
  },
  mounted(){
    this.loadQuestionByPosition();
    this.token = participationStorageService.getAccessToken();
  },
  methods: {
    async loadQuestionByPosition(){
      await quizApiService.getQuestion(this.position).then((response) => {
        this.question = response.data;      
      })
    }
  }
}
</script>
