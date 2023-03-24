<style>
@import '../assets/css/questionList.css';
</style>

<template>
    <div class="question-wrapper">
        <h1>Questions</h1>
        <button @click="goToCreate">Créer une question</button>
        
        <div v-for="(question, index) in questions" class="question" @click="$emit('question-selected', question.position)">
            <p>{{index+1}})</p>
            <p>{{question.text}}</p>             
        </div>
    </div>
  
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "../services/ParticipationStorageService";

export default {
    name: "QuestionList",
    data() {
        return {
        questions: [],
        token: null
        };
    },
    async created() {

        this.token = participationStorageService.getAccessToken();

        if(this.token == null){
            this.$router.push('/admin');
        }

        await quizApiService.getAllQuestions().then((response) => {
            this.questions = response.data.questions
        })
    },
    methods: {
        goToCreate(){
            this.$router.push("/create-question")
        }
    }
}
</script>
