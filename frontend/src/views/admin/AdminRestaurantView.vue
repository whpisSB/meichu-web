<template>
  <WarningDialog v-if="showWarningDialog" message="已成功登出"></WarningDialog>
  <SuccessDialog v-if="showSuccessDialog" message="刪除成功"></SuccessDialog>
  <EditMealDialog v-if="editMealDialog" @close="close()" @sub="comfirmUpdateMealPrice()"> </EditMEalDialog>
  <AddMealDialog v-if="addMealDialog" @close="close()" @subm="addNewMeal()"> </AddMealDialog>
  <DeleteMealDialog v-if="showDeleteDialog" @close="close()" @subm="confirmDeleteMeal"> </DeleteMealDialog>
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse gap-4 lg:flex-row">
      <AdminSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></AdminSidebar>

      <div class="w-full lg:w-5/6">
        <div class="px-5 py-6 text-4xl font-bold">
          {{ restaurantInfo?.restaurant }}
        </div>
        <div class="mr-auto items-center justify-between sm:flex">
          <div class="mb-4 px-5 text-lg font-bold">
            營業時間: {{ restaurantInfo?.open_time }} - {{ restaurantInfo?.close_time }}
          </div>
          <div class="mb-4 px-5 text-lg font-bold">電話: {{ restaurantInfo?.phone }}</div>
          <button
            @click="addMealDialog = true"
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
            <p class="text-lg font-medium leading-none text-gray-700">新增餐點</p>
          </button>
        </div>
        <div class="mt-5 grid  grid-cols-4 gap-4  px-5">
          <div
            style="cursor: pointer"
            class="flex h-auto flex-col justify-between rounded-md border bg-white px-1 py-3"
            v-for="meal in restaurantMeals"
          >
            <div class="px-4 py-4">
              <div class="font-bold text-gray-800">{{ meal.name }}</div>
              <div class="font-bold text-gray-800" v-if="meal.combo == false">單點</div>
              <div class="font-bold text-gray-800" v-else>套餐</div>
            </div>
            <div class="py-4 flex flex-row items-center justify-between">
              <span class="self-end px-4 text-lg font-bold text-yellow-500">${{ meal.price }}</span>
              <img :src="'/api' + meal.picture" class="mr-9 h-14 w-14 rounded-md object-cover" alt="" />
            </div>
            <div class="px-4 py-4 inline-flex items-center justify-cente">
              <button
                @click="deleteMeal(meal)"
                type="button"
                class="inline-flex  rounded-lg border border-red-400 bg-red-300 px-10 py-2.5 text-sm font-medium text-black hover:bg-white focus:outline-none focus:ring-4"
              >
                
                刪除
              </button>
              <button
                @click="updateMealPrice(meal)"
                type="button"
                class="ml-auto mx-4 inline-flex rounded-lg border border-orange-400 bg-orange-200 px-10 py-2.5 text-sm font-medium text-black hover:bg-white focus:outline-none focus:ring-4"
              >
                編輯價格
              </button>
            </div>
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
import adminService from '@/service/adminService'
const useRestaurant = useRestaurantStore()
const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore)
const route = useRoute()
const restaurantInfo = ref<restaurant>()
const restaurantMeals = ref<meal[]>([])
const addMealDialog = ref(false)
const { mealInfo, restaurantId } = storeToRefs(useRestaurant)
// const addMealDialog = ref(false)
const showSuccessDialog = ref(false)
const editMealDialog = ref(false)
const showDeleteDialog = ref(false)
const { mealPrice, available_dish_id, checkHasUpload } = storeToRefs(useRestaurant)
const showWarningDialog = ref(false)
const timer = ref()

const currentChoose = ref(0)
onMounted(async () => {
  checkHasUpload.value = false
  const OuthResult = await userService.userCheckOuth()
  if (OuthResult === false) {
    alert('請重新登入')
    router.push('/')
  }
  await getRestaurant()
})

const getRestaurant = async () => {
  available_dish_id.value = []
  restaurantInfo.value = await workerService.getRestaurant(userInfo.value.outh_token, restaurantId.value.toString())
  restaurantMeals.value = restaurantInfo.value.meals
  for (let i = 0; i < restaurantMeals.value.length; i++) {
    available_dish_id.value.push(restaurantMeals.value[i].dish_id)
  }
}
const close = () => {
  addMealDialog.value = false
  editMealDialog.value = false
  showDeleteDialog.value = false
}

const updateMealPrice = (meal: meal) => {
  mealPrice.value.dish_id = meal.dish_id
  mealPrice.value.updated_price = meal.price
  console.log(mealPrice.value)
  editMealDialog.value = true
}

const addNewMeal = async () => {
  // console.log(restaurantId[0])

  // console.log(restaurantId[0])
  console.log(mealInfo.value)
  mealInfo.value.restaurant_id = restaurantId.value.toString()
  if (mealInfo.value.picture === null || 
      mealInfo.value.picture === '' || 
      mealInfo.value.picture === undefined || 
      mealInfo.value.description === '' ||
      mealInfo.value.name === '' ||
      mealInfo.value.price === 0) {
    console.log('no')
    checkHasUpload.value = true    
    return
  }
  addMealDialog.value = false
  await adminService.addNewMeal(userInfo.value.outh_token, mealInfo.value)
  await getRestaurant()
  addMealDialog.value = false
  mealInfo.value = {
    restaurant_id: '',
    name: '',
    price: 0,
    description: '',
    picture: null,
    picture_filename: '',
    combo: 0
  }
  checkHasUpload.value = false
}

const comfirmUpdateMealPrice = async () => {
  await adminService.updateMealPrice(userInfo.value.outh_token, mealPrice.value)
  await getRestaurant()
  editMealDialog.value = false
}

const deleteMeal = (meal: meal) => {
  showDeleteDialog.value = true
  currentChoose.value = meal.dish_id
}

const confirmDeleteMeal = async () => {
  available_dish_id.value.splice(available_dish_id.value.indexOf(currentChoose.value), 1) 
  await adminService.updateMenu(userInfo.value.outh_token, available_dish_id.value)
  await getRestaurant()
  showDeleteDialog.value = false
}
// const close = () => {
//   addMealDialog.value = false
// }

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
