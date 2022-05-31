import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import StartQuiz from '../views/StartQuiz.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/start-quiz",
      name: "StartQuiz",
      component: StartQuiz,
    }
  ]
})

export default router
