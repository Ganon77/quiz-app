<style>
@import '../assets/css/admin.css';
</style>

<template>
    <template v-if="token == null">
        <form method="post" class="login-form" @submit="login">
            <div class="login-container">
                <div class="login-wrapper">
                    <label for="pwd">Mot de passe</label>
                    <input v-model="password" class="pwd-input" type="password" name="pwd"/>
                </div>                
                <input class="submit-login" type="submit" value="Connexion"/>
            </div>
        </form>
    </template>
    <template v-else>
        <QuestionListVue @question-selected="goToQuestion"></QuestionListVue>
        <router-view></router-view>
    </template>
</template>

<script>

import quizApiService from "@/services/quizApiService";
import participationStorageService from "../services/ParticipationStorageService";
import QuestionListVue from "../components/QuestionList.vue";
import jwt_decode from 'jwt-decode';

export default {
  name: "Admin",
  data() {
    return {
        token: null,
        password: ""
    };
  },
  async created() {
        this.token = participationStorageService.getAccessToken();

        var decoded = jwt_decode(this.token);

        var currentTime = Math.round(+new Date()/1000);

        if(currentTime > decoded.exp){
            participationStorageService.deleteAccessToekn();
            this.token = null;
        }
  },
  components: {
    QuestionListVue
  },
  methods: {
      async login(e) {
          e.preventDefault()
          const payload = {
              "password": this.password
          }

          quizApiService.login(JSON.stringify(payload)).then((response) => {
              try{
                this.token = response.data.token;
                participationStorageService.saveAccessToken(this.token);
              }               
              catch{
                  alert("Wrong password");
              }
              
          })
      },
      goToQuestion(position) {
            this.$router.push(`/question-display/${position}`);
      }
  }
};
</script>