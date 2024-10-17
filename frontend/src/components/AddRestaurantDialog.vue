<template>
  <div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <div class="fixed inset-0 bg-gray-50 bg-opacity-75 transition-opacity"></div>

    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="mx-auto mt-20 max-w-xl overflow-hidden rounded-2xl bg-gray-50 shadow-lg">
        <div class="bg-yellow-400 px-6 py-4 text-center text-2xl font-bold uppercase text-gray-600">新增餐廳</div>
        <div class="px-6 py-4">
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700"> 餐廳名稱 </label>
            <input
              v-model="restaurantInfo.restaurant_name"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              placeholder="輸入餐廳名稱(必填)"
            />
          </div>
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700"> 餐廳聯絡電話 </label>
            <input
              v-model="restaurantInfo.phone"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              placeholder="輸入餐廳聯絡電話(必填)"
            />
          </div>
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700"> 營業開始時間 </label>
            <input
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              v-model="restaurantInfo.open_time"
              type="time"
              placeholder="Select a time"
            />
          </div>
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700"> 營業結束時間 </label>
            <input
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              v-model="restaurantInfo.close_time"
              type="time"
              placeholder="Select a time"
            />
          </div>
          <!-- <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700" for="service"> Service </label>
            <select
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              id="service"
              name="service"
            >
              <option value="">Select a service</option>
              <option value="haircut">Haircut</option>
              <option value="coloring">Coloring</option>
              <option value="styling">Styling</option>
              <option value="facial">Facial</option>
            </select>
          </div> -->
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700" for="message"> 照片 </label>
            <input type="file" id="input" @change="handleFiles" accept="image/png, image/gif, image/jpeg" />
          </div>
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700" for="message"> 餐廳描述 </label>
            <textarea
              v-model="restaurantInfo.description"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              id="message"
              rows="4"
              placeholder="餐廳額外資訊"
            ></textarea>
          </div>

          <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="phone"> 餐點價錢 </label> -->
            <label class="mb-2 block text-red-600 text-center" v-if="checkHasUploadRestaurant == true"> 有空白處尚未填寫或照片還沒有上傳 </label>
          </div>
          <div class="space-y-2">
            <div aria-hidden="true" class="border-t px-2 dark:border-gray-700"></div>

            <div class="px-6 py-2">
              <div class="grid grid-cols-[repeat(auto-fit,minmax(0,1fr))] gap-2">
                <button
                  @click="$emit('close')"
                  class="focus:ring-primary-600 focus:text-primary-600 focus:bg-primary-50 focus:border-primary-600 dark:focus:text-primary-400 dark:focus:border-primary-400 inline-flex min-h-[2.25rem] items-center justify-center gap-1 rounded-lg border border-gray-300 bg-white px-4 py-1 text-sm font-medium text-gray-800 outline-none transition-colors hover:bg-gray-50 focus:ring-2 focus:ring-inset focus:ring-offset-2 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 dark:hover:border-gray-500 dark:hover:bg-gray-700 dark:focus:bg-gray-800 dark:focus:ring-offset-0"
                >
                  <span class="flex items-center gap-1">
                    <span class=""> Cancel </span>
                  </span>
                </button>

                <button
                  @click="$emit('sub')"
                  class="inline-flex min-h-[2.25rem] items-center justify-center gap-1 rounded-lg border border-transparent bg-red-600 px-4 py-1 text-sm font-medium text-white shadow outline-none transition-colors hover:bg-red-500 focus:bg-red-700 focus:ring-2 focus:ring-inset focus:ring-white focus:ring-offset-2 focus:ring-offset-red-700 dark:focus:ring-offset-0"
                >
                  <span class="flex items-center gap-1">
                    <span class=""> Confirm </span>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRestaurantStore } from '@/store/restaurant'
import { storeToRefs } from 'pinia'
const useRestaurant = useRestaurantStore()
const { restaurantInfo, checkHasUploadRestaurant } = storeToRefs(useRestaurant)
import { useUserStore } from '@/store/user'
const userStore = useUserStore()
import adminService from '@/service/adminService'
const { userInfo } = storeToRefs(userStore)
const data = ref()

const test = new FormData()
const handleFiles = async (e: any) => {
  restaurantInfo.value.picture = e.target.files[0]
}
</script>

<style></style>
