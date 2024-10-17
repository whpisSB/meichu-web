<template>
  <!-- <OrderDetailDialog v-if="historyOrderDialog" @close="close()"></OrderDetailDialog> -->
  <WarningDialog v-if="showWarningDialog" message="已成功登出"></WarningDialog>
  <OrderDetailDialog :dishes="orderDishes" v-if="historyOrderDialog" @close="close()"></OrderDetailDialog>
  <RateOrderDialog v-if="showDialog" @close="submitReview()"></RateOrderDialog>
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse lg:flex-row">
      <WorkerSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></WorkerSidebar>
      <div class="w-full lg:w-5/6">
        <div class="px-4 py-4 md:px-10 md:py-7">
          <h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Order history</h1>
        </div>
        <div class="bg-white px-4 py-4 md:px-8 md:py-7 xl:px-10">
          <div class="items-center justify-between sm:flex">
            <div
              class="flex cursor-pointer items-center rounded bg-gray-200 px-4 py-3 text-sm font-medium leading-none text-gray-600 hover:bg-gray-300"
            >
              <p>Sort By:</p>
              <select aria-label="select" class="ml-1 bg-transparent focus:text-indigo-600 focus:outline-none">
                <option class="text-sm text-indigo-800">Latest</option>
                <option class="text-sm text-indigo-800">Oldest</option>
                <option class="text-sm text-indigo-800">Latest</option>
              </select>
            </div>
          </div>
          <div class="mt-7 overflow-x-auto">
            <table class="w-full whitespace-nowrap">
              <tbody>
                <tr tabindex="0" class="h-16 rounded border border-gray-300 focus:outline-none">
                  <td class="pl-5"></td>
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="mr-2 text-base font-medium leading-none text-gray-700">餐廳名稱</p>
                    </div>
                  </td>
                  <td class="pl-24">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">總共消費金額</p>
                    </div>
                  </td>
                  <td class="pl-5"></td>
                  <td class="pl-5"></td>
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">訂餐日期日期</p>
                    </div>
                  </td>
                  <!-- <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">訂餐日期日期</p>
                    </div>
                  </td> -->
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">餐廳評分</p>
                    </div>
                  </td>
                  <td class="pl"></td>

                  <td>
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">評分此餐廳</p>
                    </div>
                  </td>
                  <td class="pl-4">
                    <!-- <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">明細</p> -->
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">明細</p>
                    </div>
                  </td>
                </tr>
                <tr v-for="(order, index) in orders" class="h-16 rounded border border-gray-300 focus:outline-none">
                  <td class="pl-4">{{ index + 1 }}</td>
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="mr-2 text-base font-medium leading-none text-gray-700">
                        {{ order.restaurant_name }}
                      </p>
                    </div>
                  </td>
                  <td class="pl-24">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">$ {{ order.total_price }}</p>
                    </div>
                  </td>
                  <td class="pl-5"></td>
                  <td class="pl-5"></td>
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">
                        {{ order.order_time }}
                      </p>
                    </div>
                  </td>
                  <!-- <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">
                        {{ order.order_time }}
                      </p>
                    </div>
                  </td> -->
                  <td class="pl-5">
                    <div class="flex items-center">
                      <p class="ml-2 text-sm leading-none text-gray-600">
                        {{ order.overall_rating }}
                      </p>
                    </div>
                  </td>
                  <td class="pl"></td>

                  <td>

                    <button
                      v-if="order.overall_rating <= 0"
                      @click="openDialog(index)"
                      class="rounded bg-gray-100 px-5 py-3 text-sm leading-none text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2"
                    >
                      rate order
                    </button>
                    <button
                      v-else
                      @click="openDialog(index)"
                      disabled
                      class="rounded bg-gray-100 px-5 py-3 text-sm leading-none text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2"
                    >
                      已評分
                    </button>
                  </td>
                  <td class="pl-4">
                    <button

                      @click="historyOrderDialog = true, orderDishes = order.dishes"
                      class="rounded bg-gray-100 px-5 py-3 text-sm leading-none text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2"
                    >
                      View
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

<script lang="ts" setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import workerService from '@/service/workerService'
import userService from '@/service/userService'
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'
import router from '@/router'


const showWarningDialog = ref(false)
const timer = ref()
const orderStore = useOrderStore()
const userStore = useUserStore()
const historyOrderDialog = ref(false)
// const historyOrderDialog = ref(false)
const { userInfo } = storeToRefs(userStore)
const showDialog = ref(false)
const { orders, selectIndex, overAllRating } = storeToRefs(orderStore)
const orderDishes = ref<any[]>([]);

onMounted(async () => {
  const OuthResult = await userService.userCheckOuth()
  if (OuthResult === false) {
    alert('請重新登入')
    router.push('/')
  }
  await getHistortOrder()
})

const getHistortOrder = async () => {
  const data = await workerService.getHistoryOrder(userInfo.value.outh_token)
  orders.value = data
  console.log(orders.value)
}

const openDialog = (index: number) => {
  selectIndex.value = index
  showDialog.value = true
}

const close = () => {
  showDialog.value = false
  historyOrderDialog.value = false
}
const submitReview = async () => {
  const orderID = orders.value[selectIndex.value].order_id
  await workerService.reviewOrder(
    userInfo.value.outh_token,
    orderID,
    overAllRating.value,
    orders.value[selectIndex.value]
  )
  await getHistortOrder()
  console.log(orders.value)
  showDialog.value = false
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
