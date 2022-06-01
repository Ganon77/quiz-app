
<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>

<script>
import QuestionDisplay from "./QuestionDisplay.vue"
import quizApiService from "@/services/quizApiService";

export default {
  name: "QuestionManager",
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 1,
      currentQuestion: null
    };
  },
  components: {
    QuestionDisplay
  },
  async created() {
    await quizApiService.getQuestion(this.currentQuestionPosition).then((response) => {
      this.currentQuestion = response.question
      this.totalNumberOfQuestion = response.size
    })
  }
}
</script>
