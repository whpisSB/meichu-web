<template>
  <WarningDialog v-if="showWarningDialog" message="已成功登出"></WarningDialog>
  
  <AddRestaurantDialog v-if="addRestaurantDialog" @close="close()" @sub="addRestaurant()"> </AddRestaurantDialog>
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse lg:flex-row">
      <AdminSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></AdminSidebar>
      <div class="bg-white-100 lg:w-6/6 min-h-screen w-full">
        <!-- header -->
        <div class="mt-5 flex flex-row items-center justify-center px-5">
          <div class="text-gray-800">
            <div class="text-3xl font-bold">餐廳選擇</div>
          </div>
        </div>
        <div class="mt-5 items-center justify-between sm:flex">
          <button
            @click="openAddRestaurantDailog()"
            class="text-items-center ml-auto mr-5 inline-flex justify-center rounded-lg border border-blue-400 bg-blue-200 px-8 py-4 hover:bg-white focus:ring-2"
          >
            <svg
              class="mr-1 h-5 w-5 text-gray-800"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <line x1="12" y1="8" x2="12" y2="16" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
            <p class="text-lg font-medium leading-none text-gray-700">新增餐廳</p>
          </button>
        </div>

        <!-- end categories -->
        <!-- products -->
        <div class="mt-5 grid grid-cols-4 gap-4 overflow-y-auto px-5">
          <div
            class="bg-white-100 border-black-800 flex flex-col justify-between rounded-2xl border px-2 py-2 shadow-lg"
            v-for="restaurant in restaurants"
          >
            <a @click="goToRestaurant(restaurant)">
              <div class="relative">
                <img
                  class="aspect-[3/2] h-1/2 w-full"
                  :src="'/api' + restaurant.picture"
                  alt="Sunset in the mountains"
                />
              </div>
              <div class="px-1 py-1">
                <p>{{ restaurant.restaurant }}</p>
                <div class="mt-2 flex items-center">
                  <svg
                    class="me-1 h-4 w-4 text-yellow-300"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 22 20"
                  >
                    <path
                      d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                    />
                  </svg>
                  <p class="ms-2 text-sm font-bold text-gray-900">{{ restaurant.rating }}</p>
                </div>
              </div>
            </a>
          </div>
        </div>

        <!-- end products -->
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import AdminSidebar from '../../components/AdminSidebar.vue'
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import restaurantService from '@/service/restaurantService'
import workerService from '@/service/workerService'
import userService from '@/service/userService'
import type { restaurant } from '@/types/worker'
import { useUserStore } from '@/store/user'
import router from '@/router'
import { useRestaurantStore} from '@/store/restaurant'
import adminService from '@/service/adminService'

const restaurants = ref<restaurant[]>([])
const addRestaurantDialog = ref(false)
const { userInfo } = storeToRefs(useUserStore())
const { restaurantInfo, checkHasUploadRestaurant, restaurantId } = storeToRefs(useRestaurantStore())
const showWarningDialog = ref(false)
const timer = ref()
onMounted(async () => {
  checkHasUploadRestaurant.value = false
  const OuthResult = await userService.userCheckOuth()
  if (OuthResult === false) {
    alert('請重新登入')
    router.push('/')
  }
  await getRestaurantList()
  for (let i = 0; i < restaurants.value.length; i++) {
    restaurants.value[i].url = '/admin/restaurant/' + restaurants.value[i].id
  }
  console.log(restaurants.value)
})

const getRestaurantList = async () => {
  const data = await workerService.getRestaurantList(userInfo.value.outh_token)
  restaurants.value = data
}

const openAddRestaurantDailog = async () => {
  addRestaurantDialog.value = true
}

const close = () => {
  addRestaurantDialog.value = false
}

const addRestaurant = async () => {
  console.log(restaurantInfo.value)
  if (restaurantInfo.value.close_time === '' || restaurantInfo.value.open_time === '' || 
  restaurantInfo.value.phone === '' || restaurantInfo.value.restaurant_name === '' || restaurantInfo.value.picture === null) {
    checkHasUploadRestaurant.value = true
    console.log('quit')
    return
  }
  checkHasUploadRestaurant.value = false
  await adminService.addNewRestaurant(userInfo.value.outh_token, restaurantInfo.value)
  await getRestaurantList()
  addRestaurantDialog.value = false
  restaurantInfo.value = {
    open_time: '11:00',
    close_time: '20:00',
    restaurant_name: '',
    phone: '',
    description: '',
    picture: null
  }
}

const goToRestaurant = (restaurant: restaurant) => {
  restaurantId.value = restaurant.id
  router.push('/admin/restaurant/' + restaurant.id)
}

watch(userInfo, () => {
  if (userInfo.value.outh_token === '') {
    showWarningDialog.value = true
    timer.value = setTimeout(() => {
      showWarningDialog.value = false
      clearTimeout(timer.value)
      router.push('/')
    }, 1000)
  }
})
</script>

<style></style>
