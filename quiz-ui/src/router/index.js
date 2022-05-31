import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import StartQuiz from '../views/StartQuiz.vue'
import Questions from '../views/Questions.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/about",
      name: "StartQuiz",
      component: StartQuiz,
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
    }
  ]
})

export default router
