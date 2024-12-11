import { createRouter, createWebHashHistory } from 'vue-router'
import PaperExtractView from '../views/PaperExtractView.vue'
import ResearchAgent from '../views/ResearchAgent.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PaperExtractView
    },
    {
      path: '/agent',
      name: 'agent',
      component: ResearchAgent
    },
    {
      path: '/extract',
      name: 'extract',
      component: PaperExtractView
    }
  ]
})

export default router
