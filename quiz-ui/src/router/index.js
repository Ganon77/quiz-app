import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import StartQuiz from '../views/StartQuiz.vue'
import Questions from '../views/Questions.vue'
import Score from '../views/Score.vue'
import Admin from '../views/Admin.vue'
import AdminQuestionDisplay from '../views/AdminQuestionDisplay.vue'
import EditQuestion from '../views/EditQuestion.vue'
import CreateQuestion from '../views/CreateQuestion.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/admin",
      name: "Admin",
      component: Admin,
    },    
    {
      path: "/question-display/:position",
      name: "AdminQuestionDisplay",
      props: true,
      component: AdminQuestionDisplay,
    },
    {
      path: "/edit-question/:position",
      name: "EditQuestion",
      props: true,
      component: EditQuestion,
    },
    {
      path: "/create-question",
      name: "CreateQuestion",
      props: true,
      component: CreateQuestion,
    },
    {
      path: "/start-quiz",
      name: "StartQuiz",
      component: StartQuiz,
    },
    {
      path: "/questions",
      name: "Questions",
      component: Questions,
    },
    {
      path: "/score",
      name: "Score",
      component: Score,
    }
  ]
})

export default router
