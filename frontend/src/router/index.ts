import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CreateArticleView from '../views/CreateArticleView.vue';
import NotFoundView from '../views/NotFoundView.vue'; // Add a NotFoundView component

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/create',
      name: 'create',
      component: CreateArticleView,
    },
    {
      path: '/articles/:name',
      name: 'article-detail',
      component: () => import('../views/ArticleDetailView.vue'),
    },
    // Add the catch-all route at the end
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
});

export default router;
