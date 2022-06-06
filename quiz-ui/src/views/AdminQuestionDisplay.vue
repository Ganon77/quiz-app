<style>
</style>

<template v-if="token != null">
  <div>
    <QuestionDisplay v-if="question" :question="question" :isAdmin="true" v-bind:is="QuestionDisplay" @delete-selected="deleteClickedHandler"/>
  </div>
</template>

<script>
import QuestionDisplay from "../components/QuestionDisplay.vue"
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import jwt_decode from 'jwt-decode';

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
      this.token = participationStorageService.getAccessToken();

      var decoded = jwt_decode(this.token);

      var currentTime = Math.round(+new Date()/1000);

      if(currentTime > decoded.exp){
          participationStorageService.deleteAccessToekn();
          this.$router.push("/admin");
      }

      this.loadQuestionByPosition();
  },
  methods: {
    async loadQuestionByPosition(){
      await quizApiService.getQuestion(this.position).then((response) => {
        this.question = response.data;      
      })
    },
    async deleteClickedHandler(){
      await quizApiService.deleteQuestion(this.token, this.position).then((response) => {
        this.$router.push("/admin")     
      })
    }
  }
}
</script>
