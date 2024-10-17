<template>

  <WarningDialog v-if="showWarningDialog" message="已成功登出"></WarningDialog>
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse lg:flex-row">
      <WorkerSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></WorkerSidebar>

      <div class="w-full lg:w-5/6">
        <div class="px-5 py-6 text-4xl font-bold">
          {{ restaurantInfo?.restaurant }}
        </div>
        <div class="mr-auto items-center justify-between sm:flex">
          <div class="mb-4 px-5 text-lg font-bold">
            營業時間: {{ restaurantInfo?.open_time }} - {{ restaurantInfo?.close_time }}
          </div>
          <div class="mb-4 px-5 text-lg font-bold">電話: {{ restaurantInfo?.phone }}</div>
          <div class="text-items-center ml-auto mr-5 inline-flex justify-center rounded-lg border"></div>
        </div>
        <div class="mt-5 grid  grid-cols-4 gap-4 h-auto px-5">
          <div
            style="cursor: pointer"
            class="flex  flex-col justify-between rounded-md border bg-white px-1 py-3"
            v-for="meal in restaurantMeals"
          >
            <div class="px-4 py-4">
              <div class="font-bold text-gray-800">{{ meal.name }}</div>
              <div class="font-bold text-gray-800" v-if="meal.combo == false">單點</div>
              <div class="font-bold text-gray-800" v-else>套餐</div>
             
            </div>
            <div class="px-4 py-4 flex flex-row items-center justify-between">
              <div class="font-bold text-gray-800">description: {{ meal.description }}</div>
            </div>

            <div class="flex flex-row items-center justify-between">
              <span class="self-end px-4 text-lg font-bold text-yellow-500">${{ meal.price }}</span>
              <img :src="'/api' + meal.picture" class="mr-4 h-14 w-14 rounded-md object-cover" alt="" />
            </div>

          
            <!-- <button
              type="button"
              class="mx-4 mb-3 inline-flex items-center justify-center rounded-lg border border-orange-400 bg-orange-200 px-5 py-2.5 text-sm font-medium text-black hover:bg-white focus:outline-none focus:ring-4"
            >
              <svg
                class="-ms-2 me-2 h-5 w-5"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 4h1.5L9 16m0 0h8m-8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm-8.5-3h9.25L19 7h-1M8 7h-.688M13 5v4m-2-2h4"
                />
              </svg>
              Edit
            </button> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import workerService from '@/service/workerService'
import userService from '@/service/userService'
import { useUserStore } from '@/store/user'
import { useRestaurantStore } from '@/store/restaurant'
import type { restaurant, meal } from '@/types/worker'
import router from '@/router'

const useRestaurant = useRestaurantStore()
const showWarningDialog = ref(false)
const timer = ref()
const userStore = useUserStore()

const { restaurantId } = storeToRefs(useRestaurant)
const { userInfo } = storeToRefs(userStore)
const route = useRoute()
const restaurantInfo = ref<restaurant>()
const restaurantMeals = ref<meal[]>([])

onMounted(async () => {
  const OuthResult = await userService.userCheckOuth()
  if (OuthResult === false) {
    alert('請重新登入')
    router.push('/')
  }
  await getRestaurant()
})

const getRestaurant = async () => {
  console.log('cute')
  restaurantInfo.value = await workerService.getRestaurant(userInfo.value.outh_token, restaurantId.value.toString())
  restaurantMeals.value = restaurantInfo.value.meals
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
