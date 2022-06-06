<style>
@import '../assets/css/edit.css';
</style>

<template v-if="isAdmin">
  <div v-if="question" class="answer-container">
    <form class="edit-form" @submit.prevent="updateQuestion">
        <div class="input-wrapper">

            <div class="input-container">
                <label for="postion">Position</label>
                <input type="number" placeholder="Position" name="position" step="1" min="1" :max="totalNumberOfQuestion" v-model="position"/>
            </div>
            

            <div class="input-container">
                <label for="titre">Titre</label>
                <input type="text" placeholder="Titre" name="titre" v-model="question.title">
            </div>

            <div class="input-container">
                <label for="text">Intitulé</label>
                <input type="text" placeholder="Intitulé" name="text" v-model="question.text">
            </div>            
        </div>       
        <h1>Réponses Possible</h1>
        <div class="answer-wrapper">   
            <template v-if="question.possibleAnswers.length > 0">
                <div v-for="(answer, index) in question.possibleAnswers" class="answer-input">
                    <div v-if="answer.isCorrect"  class="goodAnswer ">
                        <input type="radio" class="select" v-model="selected" v-bind:value="answer" name="answers" @change="onChange($event)" checked/>
                        <input class="answerText" v-bind:name="'answer'+(index+1)" v-model="answer.text"/>
                    </div>
                    <div v-else class="wrongAnwser">
                        <input type="radio" class="select" v-model="selected" v-bind:value="answer" name="answers" @change="onChange($event)"/>
                        <input class="answerText" v-bind:name="'answer'+(index+1)" v-model="answer.text"/>
                    </div>
                </div>
            </template>
            <template v-else>
                <div v-for="i in 4">
                    <div class="wrongAnwser">
                        <input type="radio" class="select" v-model="selected" v-bind:value="answer" name="answers" @change="onChange($event)"/>
                        <input class="answerText" v-bind:name="'answer'+i"/>
                    </div>
                </div>
            </template>    
        </div>

        <div class="image-container">
            <ImageUploadVue @file-change="imageFileChangedHandler" />
            <img v-bind:src="image"/>
        </div>
        
        <div class="submit-container">
            <input class="submit" type="submit" value="Modifier"/>
            <button class="submit" @click="cancel">Annuler</button>
        </div>
        
    </form> 
  </div>  
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import ImageUploadVue from "../components/ImageUpload.vue";
import jwt_decode from 'jwt-decode';

export default {
  name: "EditQuestion",
  data() {
    return {
        token: null,
        question: null,
        position: null,
        totalNumberOfQuestion: 1,
        image: null,
        selected: null,
        answer: null
    };
  },
  components : {
      ImageUploadVue
  },
  async created(){

        this.token = participationStorageService.getAccessToken();
        var decoded = jwt_decode(this.token);

        var currentTime = Math.round(+new Date()/1000);

        if(currentTime > decoded.exp){
            participationStorageService.deleteAccessToekn();
            this.$router.push("/admin");
        }

      await quizApiService.getQuizInfo().then((response) => {
        this.totalNumberOfQuestion = response.data.size;
    })
    this.loadQuestionByPosition();
    
  },
  methods: {
    async loadQuestionByPosition(){
      await quizApiService.getQuestion(this.$route.params.position).then((response) => {
        this.question = response.data;
        this.image = this.question.image;
        this.position = this.question.position
      })
    },
    onChange(event) {
        var optionText = event.target.parentElement;
        const el = document.body.getElementsByClassName('goodAnswer');
        el[0].classList.add('wrongAnwser');
        el[0].classList.remove('goodAnswer');        
        optionText.classList.add("goodAnswer");
    },
    imageFileChangedHandler(b64String) {
        this.image = b64String;
    },
    async updateQuestion(submitEvent){
        const body = {
            "text": submitEvent.target.elements.text.value,
            "title": submitEvent.target.elements.titre.value,
            "image": this.image,
            "position": this.position,
            "possibleAnswers": [
                {
                    "text": submitEvent.target.elements.answer1.value,
                    "isCorrect": this.selected.text === submitEvent.target.elements.answer1.value,
                },
                {
                    "text": submitEvent.target.elements.answer2.value,
                    "isCorrect": this.selected.text === submitEvent.target.elements.answer2.value,
                },
                {
                    "text": submitEvent.target.elements.answer3.value,
                    "isCorrect": this.selected.text === submitEvent.target.elements.answer3.value,
                },
                {
                    "text": submitEvent.target.elements.answer4.value,
                    "isCorrect": this.selected.text === submitEvent.target.elements.answer4.value,
                }
            ]
        };

        await quizApiService.changeQuestion("PUT", JSON.stringify(body), this.token, this.$route.params.position).then((response) => {
            this.$router.push("/question-display/"+this.position)
        })
    },
    cancel(){
        this.$router.push("/question-display/"+this.$route.params.position)
    }
  }
}
</script>
