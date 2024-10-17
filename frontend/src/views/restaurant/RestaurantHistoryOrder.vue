<template>
  <!-- component -->
  <WarningDialog v-if="showWarningDialog" message="已成功登出"></WarningDialog>
  
  <successDialog v-if="showDialog" @close="close()" message="Yo have finish these order"></successDialog>
  <OrderDetailDialog :dishes="orderDishes" v-if="historyOrderDialog" @close="close()"></OrderDetailDialog>

  <!-- <OrderDetailDialog v-if="historyOrderDialog" @close="close()"></OrderDetailDialog> -->

  <!-- <successDialog restaurant"showDialog" @close="close()" message="Yo have success submit the order"></successDialog> -->
  <div class="mx-auto bg-white">
    <!-- component -->
    <div class="flex flex-col-reverse lg:flex-row">
      <RestaurantSidebar class="min-h-screen w-full justify-start shadow-lg lg:w-1/6"></RestaurantSidebar>

      <div class="w-full lg:w-5/6">
        <div class="px-4 py-4 md:px-10 md:py-7">
          <div class="flex items-center justify-between">
            <p
              tabindex="0"
              class="text-base font-bold leading-normal text-gray-800 focus:outline-none sm:text-lg md:text-xl lg:text-2xl"
            >
              訂單狀況
            </p>
          </div>
        </div>
        <div class="bg-white px-4 py-4 md:px-8 md:py-7 xl:px-10">
          <div class="items-center justify-between sm:flex">
            <div class="flex items-center">
              <!-- <button -->
              <button
                class="rounded-full focus:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-800"
                href=" javascript:void(0)"
                @click="selectType = 'All'"

              >
                <div v-if="selectType == 'All'" class="rounded-full bg-indigo-100 px-8 py-2 text-indigo-700">
                  <p>All</p>
                </div>
                <div v-else class="rounded-full px-8 py-2 text-gray-600 hover:bg-indigo-100 hover:text-indigo-700">
                  <p>All</p>
                </div>
              </button>
              <!-- <button
              </button> -->
              <button
                class="ml-4 rounded-full focus:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-800 sm:ml-8"
                href="javascript:void(0)"
                @click="selectType = 'Done'"

              >
                <!-- <div v-if="selectType == 'Done'" class="rounded-full bg-indigo-100 px-8 py-2 text-indigo-700">
                  <p>Done</p>
                </div>
                <div v-else class="rounded-full px-8 py-2 text-gray-600 hover:bg-indigo-100 hover:text-indigo-700"> -->
                <div v-if="selectType == 'Done'" class="rounded-full bg-indigo-100 px-8 py-2 text-indigo-700">
                  <p>Done</p>
                </div>
                <div v-else class="rounded-full px-8 py-2 text-gray-600 hover:bg-indigo-100 hover:text-indigo-700">
                  <p>Done</p>
                </div>
              </button>
              <!-- </button> -->
              <a
                class="ml-4 rounded-full focus:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-800 sm:ml-8"
                href="javascript:void(0)"
                @click="selectType = 'Pending'"

              >
                <!-- <div v-if="selectType == 'Pending'" class="rounded-full bg-indigo-100 px-8 py-2 text-indigo-700">
                  <p>Pending</p>
                </div>
                <div v-else class="rounded-full px-8 py-2 text-gray-600 hover:bg-indigo-100 hover:text-indigo-700"> -->
                <div v-if="selectType == 'Pending'" class="rounded-full bg-indigo-100 px-8 py-2 text-indigo-700">
                  <p>Pending</p>
                </div>
                <div v-else class="rounded-full px-8 py-2 text-gray-600 hover:bg-indigo-100 hover:text-indigo-700">
                  <p>Pending</p>
                </div>
              </a>
            </div>
            <button
              v-if="finishOrderList.length != 0"
              @click="submitFinishOrder()"
              class="mt-4 inline-flex items-start justify-start rounded bg-indigo-700 px-6 py-3 hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 sm:mt-0"
            >
              <p class="text-sm font-medium leading-none text-white">完成訂單</p>
            </button>
          </div>
          <div class="mt-7 overflow-x-auto">
            <table class="w-full whitespace-nowrap">
              <tbody>
                <tr class="h-16 rounded border border-gray-100 focus:outline-none">
                  <td>
                    <div class="ml-5"></div>
                  </td>
                  <td class="">
                    <div class="flex items-center pl-5">訂單時間</div>
                  </td>
                  <td class="pl-24"></td>
                  <td class="pl-5"></td>
                  <td class="pl-5"></td>
                  <td class="pl-0">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">員工ID</p>
                    </div>
                  </td>
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">價錢</p>
                    </div>
                  </td>
                  <td class="pl-4">
                    <p class="ml-2 text-sm leading-none text-gray-600">訂單內容</p>
                  </td>
                  <td class="pl-4">
                    <p class="ml-2 text-sm leading-none text-gray-600">訂單狀態</p>
                  </td>
                </tr>
                <tr
                  v-for="order in historyOrder"
                  tabindex="0"
                  class="h-16 rounded border border-gray-100 focus:outline-none"
                >
                  <td>
                    <div class="ml-5">
                      <div
                        class="relative flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-sm bg-gray-200"
                      >
                        <input
                          type="checkbox"
                          id="checkbox"
                          v-if="order.finish === false"
                          class="h-full w-full rounded border-gray-300 bg-gray-100 text-blue-600"
                          @click="finishOrder(order.order_id)"
                        />
                        <input
                          type="checkbox"
                          id="checkbox"
                          v-else
                          class="h-full w-full rounded border-gray-300 bg-gray-100 text-blue-600"
                          disabled
                        />
                      </div>
                    </div>
                  </td>
                  <td class="">
                    <div class="flex items-center pl-5">
                      <p class="mr-2 text-base font-medium leading-none text-gray-700">{{ order.order_time }}</p>
                    </div>
                  </td>
                  <td class="pl-24"></td>
                  <td class="pl-5"></td>
                  <td class="pl-5"></td>
                  <td class="pl-0">
                    <p class="ml-2 text-sm leading-none text-gray-600">{{ order.customer_id }}</p>
                  </td>
                  <td class="pl-5">
                    <p class="ml-2 text-sm leading-none text-gray-600">${{ order.price }}</p>
                  </td>
                  <td class="pl-4">
                    <button
                      @click="historyOrderDialog = true, orderDishes = order.dishes"

                      class="rounded bg-gray-100 px-5 py-3 text-sm leading-none text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2"
                    >
                      View
                    </button>
                  </td>
                  <td class="pl-4">
                    <button
                      v-if="order.finish === true"
                      class="block w-20 rounded bg-green-100 py-3 text-sm leading-none text-green-700 focus:outline-none"
                    >
                      done
                    </button>
                    <button
                      v-else
                      class="block w-20 rounded bg-red-100 py-3 text-sm leading-none text-red-700 focus:outline-none"
                    >
                      pending
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
// import { onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import restaurantService from '@/service/restaurantService'
import type { restaurant, meal, order } from '@/types/restaurant'
import { useUserStore } from '@/store/user'
import router from '@/router'
const showWarningDialog = ref(false)
const timer = ref()
const selectType = ref('All')
// const selectType = ref('All')
const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore)
const historyOrder = ref<order[]>()
const showDialog = ref(false)
const finishOrderList = ref<number[]>([])
const historyOrderDialog = ref(false)
const orderDishes = ref<any[]>([]);
// const historyOrderDialog = ref(false)
onMounted(async () => {
  historyOrder.value = await restaurantService.getHistoryOrder(userInfo.value.outh_token)
  console.log(historyOrder.value)
})

const finishOrder = (id: number) => {
  if (finishOrderList.value.includes(id)) {
    finishOrderList.value = finishOrderList.value.filter(item => item !== id)
  } else {
    finishOrderList.value.push(id)
  }
}

const submitFinishOrder = async () => {
  console.log(finishOrderList.value)
  for (let i = 0; i < finishOrderList.value.length; i++) {
    await restaurantService.finishOrder(userInfo.value.outh_token, finishOrderList.value[i])
  }
  historyOrder.value = await restaurantService.getHistoryOrder(userInfo.value.outh_token)
  finishOrderList.value = []
  console.log(historyOrder.value)
  showDialog.value = true
}

const close = () => {
  showDialog.value = false
  historyOrderDialog.value = false
}

watch(selectType, async () => {
  if (selectType.value === 'All') {
    historyOrder.value = await restaurantService.getHistoryOrder(userInfo.value.outh_token)
  } else if (selectType.value === 'Done') {
    historyOrder.value = await restaurantService.getHistoryOrder(userInfo.value.outh_token)
    for (let i = 0; i < historyOrder.value.length; i++) {
      if (historyOrder.value[i].finish === false) {
        historyOrder.value.splice(i, 1)
        i--
      }
    }
  } else {
    historyOrder.value = await restaurantService.getHistoryOrder(userInfo.value.outh_token)
    for (let i = 0; i < historyOrder.value.length; i++) {
      if (historyOrder.value[i].finish === true) {
        historyOrder.value.splice(i, 1)
        i--
      }
    }
  }
  console.log(historyOrder.value)
})

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
