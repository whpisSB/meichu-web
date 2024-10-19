import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RestaurantView from '@/views/RestaurantView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '/',
      component: HomeView
    },
    {
      path: '/product',
      name: '/product',
      component: RestaurantView
    },
    {
      path: '/restaurant',
      name: 'Restaurant',
      component: RestaurantView
    },
    // {
    //   path: '/worker',
    //   name: 'Worker',
    //   component: () => import('@/views/worker/WorkerView.vue')
    // },
    // {
    //   path: '/history-order',
    //   name: 'History Order',
    //   component: () => import('@/views/worker/HistoryOrderView.vue')
    // },
    // {
    //   path: '/worker/restaurant/:id',
    //   name: 'WorkerRestaurant',
    //   component: () => import('@/views/worker/WorkerRestaurantView.vue')
    // },
    // {
    //   path: '/restaurant/history-order',
    //   component: () => import('@/views/restaurant/RestaurantHistoryOrder.vue')
    // },
    // {
    //   path: '/admin',
    //   component: () => import('@/views/admin/AdminView.vue')
    // },
    // {
    //   path: '/admin/restaurant/:id',
    //   component: () => import('@/views/admin/AdminRestaurantView.vue')
    // },
    // {
    //   path: '/admin/monthly-report',
    //   component: () => import('@/views/admin/AdminMonthlyReportView.vue')
    // }
    // {
    //   path: '/worker',
    //   name: 'Worker',
    //   component: () => import('@/views/WorkerView.vue')
    // },
    // {
    //   path: 'admin',
    //   name: 'Admin',
    //   component: () => import('@/views/AdminView.vue')
    // }
  ]
})

export default router
