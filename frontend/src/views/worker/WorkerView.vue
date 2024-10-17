<template>
  <WarningDialog v-if="showWarningDialog" :message="WarningMessage"></WarningDialog>
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse lg:flex-row">
      <WorkerSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></WorkerSidebar>
      <div class="bg-white-100 lg:w-6/6 min-h-screen w-full">
        <!-- header -->
        <div class="mt-5 flex flex-row items-center justify-center px-5">
          <div class="text-gray-800">
            <div class="text-3xl font-bold">餐廳選擇</div>
          </div>
        </div>

        <div class="items-center justify-between px-5 sm:flex">
          <div
            class="flex cursor-pointer items-center rounded bg-gray-200 px-4 py-3 text-sm font-medium leading-none text-gray-600 hover:bg-gray-300"
          >
            <p>Sort By:</p>
            <select aria-label="select" class="ml-1 bg-transparent focus:text-indigo-600 focus:outline-none">
              <option class="text-sm text-indigo-800">評分</option>
              <option class="text-sm text-indigo-800">價錢</option>
            </select>
          </div>
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

              <div class="px-1 py-2">
                <p class="text-sm text-gray-500">營業時間：{{ restaurant.open_time }} - {{ restaurant.close_time }}</p>
              </div>

              <div class="px-1 py-2">
                <p class="text-sm text-gray-500">價錢: $100 ~ $200</p>
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
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import workerService from '@/service/workerService'
import { useRestaurantStore } from '@/store/restaurant'
import userService from '@/service/userService'
import { useUserStore } from '@/store/user'
import type { restaurant } from '@/types/worker'
import router from '@/router'
const useRestaurant = useRestaurantStore()
const { mealInfo, restaurantId } = storeToRefs(useRestaurant)

const showWarningDialog = ref(false)
const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore)
const timer = ref()
const restaurants = ref<restaurant[]>([])
const WarningMessage = ref('已成功登出')
onMounted(async () => {
  const OuthResult = await userService.userCheckOuth()
  if (OuthResult === false) {
    alert('請重新登入')
    router.push('/')
  }
  if (userInfo.value.notify == true) {
    showWarningDialog.value = true
    WarningMessage.value = '月底已過，請記得繳費。'

    timer.value = setTimeout(() => {
      showWarningDialog.value = false
      WarningMessage.value = '已成功登出'
      userInfo.value.notify = false
      clearTimeout(timer.value)
    }, 3000)
  }
  await getRestaurantList()
  for (let i = 0; i < restaurants.value.length; i++) {
    restaurants.value[i].url = '/worker/restaurant/' + restaurants.value[i].id
  }
})

const getRestaurantList = async () => {
  const data = await workerService.getRestaurantList(userInfo.value.outh_token)
  restaurants.value = data
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

const goToRestaurant = (restaurant: restaurant) => {
  restaurantId.value = restaurant.id
  router.push('/worker/restaurant/' + restaurant.id)
}
</script>

<style></style>
