<style>
@import '../assets/css/questionManager.css';
</style>

<template>
  <div>
    <div class="bullet-wrapper">
      <template v-for="index in totalNumberOfQuestion" :key="index">
        <div class="bullet" v-bind:class="{ active: index == currentQuestionPosition}"></div>
      </template>
    </div>
    <QuestionDisplay v-if="currentQuestion" :question="currentQuestion" @answer-selected="answerClickedHandler" v-bind:is="QuestionDisplay"/>
  </div>
  
</template>

<script>
import QuestionDisplay from "./QuestionDisplay.vue"
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "QuestionManager",
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 1,
      currentQuestion: null,
      playerName: "",
      answers: []
    };
  },
  components: {
    QuestionDisplay
  },
  async created() {
    this.playerName = participationStorageService.getPlayerName();
    this.loadQuestionByPosition();

    await quizApiService.getQuizInfo().then((response) => {
      this.totalNumberOfQuestion = response.data.size;
    })
  },
  computed: {
    IsActive: function (index) {
      return index == currentQuestionPosition
    }
  },
  methods: {
    async loadQuestionByPosition(){
      await quizApiService.getQuestion(this.currentQuestionPosition).then((response) => {
        this.currentQuestion = response.data;      
      })
    },

    async answerClickedHandler(answer){
        this.answers.push(answer)
        this.currentQuestionPosition++;

        if(this.currentQuestionPosition <= this.totalNumberOfQuestion){
          this.loadQuestionByPosition()
        }
        else{
          this.currentQuestionPosition--;
          this.endQuiz();
        }
    },

    async endQuiz(){
        var payload = {
          'playerName':  this.playerName,
          'answers': this.answers
        };

        quizApiService.registerParticipation(JSON.stringify(payload)).then((response) => {
          console.log(response);
          participationStorageService.saveParticipationScore(response.data.score)
          this.$router.push('/score');
        });
    }
  }
}
</script>
