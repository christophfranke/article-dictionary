import { createRouter, createWebHistory } from 'vue-router';
import { profile } from '@/use/user'
import NotFoundView from '@/views/NotFoundView.vue';


const requireAuth = (_: unknown, __: unknown, next: Function) => {
    if (profile.isLoggedIn) {
        next();
    } else {
        next({ name: 'login' });
    }
};

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'welcome',
            component: () => import('@/views/WelcomeView.vue'),
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('@/views/HomeView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/LoginView.vue')
        },    
        {
            path: '/password-reset',
            name: 'password-reset',
            component: () => import('@/views/PasswordResetView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/views/RegisterView.vue'),
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('@/views/ProfileView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/create',
            name: 'create',
            component: () => import('@/views/CreateArticleView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/dictionary/review',
            name: 'word-review',
            component: () => import('@/views/ReviewWordView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/dictionary/:original',
            name: 'word-detail',
            component: () => import('@/views/WordDetailView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/dictionary',
            name: 'dictionary',
            component: () => import('@/views/DictionaryView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/articles',
            name: 'articles',
            component: () => import('@/views/ArticleListView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/articles/:slug/edit',
            name: 'article-edit',
            component: () => import('@/views/ArticleEditView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/articles/:slug/review',
            name: 'article-word-review',
            component: () => import('@/views/ReviewWordView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/articles/:slug',
            name: 'article-detail',
            component: () => import('@/views/ArticleDetailView.vue'),
            beforeEnter: requireAuth,
        },
        {
            path: '/articles/import/:id',
            name: 'article-import',
            component: () => import('@/views/ArticleImportView.vue'),
            beforeEnter: requireAuth,
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
