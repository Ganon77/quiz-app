<style>
@import '../assets/css/edit.css';
</style>

<template>
  <div class="answer-container">
    <form class="edit-form" @submit.prevent="updateQuestion">
        <div class="input-wrapper">

            <div class="input-container">
                <label for="postion">Position</label>
                <input type="number" placeholder="Position" name="position" step="1" min="1" :max="totalNumberOfQuestion" v-model="position"/>
            </div>
            

            <div class="input-container">
                <label for="titre">Titre</label>
                <input type="text" placeholder="Titre" name="titre" v-model="title">
            </div>

            <div class="input-container">
                <label for="text">Intitulé</label>
                <input type="text" placeholder="Intitulé" name="text" v-model="text">
            </div>            
        </div>       
        <h1>Réponses Possible</h1>
        <div class="answer-wrapper">
            <div v-for="i in 4" class="answer-input">
                <div class="wrongAnwser">
                    <input type="radio" class="select" v-model="selected" v-bind:value="answer" name="answers" @change="onChange($event)"/>
                    <input class="answerText" v-bind:name="'answer'+i"/>
                </div>
            </div>
        </div>

        <div class="image-container">
            <ImageUploadVue @file-change="imageFileChangedHandler" />
            <img v-if="image" v-bind:src="image"/>
        </div>
        
        <div class="submit-container">
            <input class="submit" type="submit" value="Ajouter"/>
        </div>
        
    </form> 
  </div>  
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import ImageUploadVue from "../components/ImageUpload.vue";
import jwt_decode from 'jwt-decode';

export default {
  name: "CreateQuestion",
  data() {
    return {
        token: null,
        position: null,
        totalNumberOfQuestion: 1,
        title: null,
        text: null,
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
    
  },
  methods: {
    onChange(event) {
        var optionText = event.target.parentElement;

        const el = document.body.getElementsByClassName('goodAnswer');

        
        if(el.length > 0){
            el[0].classList.add('wrongAnwser');
            el[0].classList.remove('goodAnswer');                   
        }

        console.log(optionText)
        
        optionText.classList.remove("wrongAnwser");
        optionText.classList.add("goodAnswer");

        this.selected = optionText.children[1].value;
        console.log(this.selected)
    },
    imageFileChangedHandler(b64String) {
        this.image = b64String;
    },
    async updateQuestion(submitEvent){
        console.log(this.selected);
        const body = {
            "text": submitEvent.target.elements.text.value,
            "title": submitEvent.target.elements.titre.value,
            "image": this.image,
            "position": this.position,
            "possibleAnswers": [
                {
                    "text": submitEvent.target.elements.answer1.value,
                    "isCorrect": this.selected === submitEvent.target.elements.answer1.value,
                },
                {
                    "text": submitEvent.target.elements.answer2.value,
                    "isCorrect": this.selected === submitEvent.target.elements.answer2.value,
                },
                {
                    "text": submitEvent.target.elements.answer3.value,
                    "isCorrect": this.selected === submitEvent.target.elements.answer3.value,
                },
                {
                    "text": submitEvent.target.elements.answer4.value,
                    "isCorrect": this.selected === submitEvent.target.elements.answer4.value,
                }
            ]
        };
                
        await quizApiService.addQuestion(JSON.stringify(body), this.token).then((response) => {
            this.$router.push("/question-display/"+this.position)
        })
    }
  }
}
</script>
