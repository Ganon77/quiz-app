
<template>
  <h1 v-if="currentQuestion">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay v-if="currentQuestion" :question="currentQuestion" @answer-selected="answerClickedHandler" v-bind:is="QuestionDisplay"/>
</template>

<script>
import QuestionDisplay from "./QuestionDisplay.vue"
import quizApiService from "@/services/quizApiService";
import participationStorageService from "../services/ParticipationStorageService";

export default {
  name: "QuestionManager",
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 1,
      currentQuestion: null,
      answers: []
    };
  },
  components: {
    QuestionDisplay
  },
  async created() {
    
    this.loadQuestionByPosition();

    await quizApiService.getQuizInfo().then((response) => {
      this.totalNumberOfQuestion = response.data.size;
    })
  }
  ,
  methods: {
    async loadQuestionByPosition(){
      await quizApiService.getQuestion(this.currentQuestionPosition).then((response) => {
        this.currentQuestion = response.data;      
      })
    },

    async answerClickedHandler(answer){
        this.answers.push(answer)
        this.currentQuestionPosition++;

        if(this.currentQuestionPosition < this.totalNumberOfQuestion){
          this.loadQuestionByPosition()
        }
        else{
          this.endQuiz()
        }
    },

    async endQuiz(){
        payload = {
          'playerName': participationStorageService.getPlayerName(),
          'answers': this.answers
        };

        quizApiService.registerParticipation(payload)
    }
  }
}
</script>
