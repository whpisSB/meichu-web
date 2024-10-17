<template>
  <div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <div class="fixed inset-0 bg-gray-50 bg-opacity-75 transition-opacity"></div>


    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="mx-auto mt-20 max-w-xl overflow-hidden rounded-2xl bg-gray-50 shadow-lg">
        <div class="bg-orange-300 px-6 py-4 text-center text-2xl font-bold uppercase text-gray-700">新增餐點</div>
        <div class="px-6 py-4">
          <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="name"> 餐點名稱 </label> -->
            <label class="mb-2 block font-bold text-gray-700" for="name"> 餐點名稱 </label>
            <input
              v-model="mealInfo.name"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              id="name"
              type="text"
              placeholder="輸入餐廳名稱(必填)"
              
            />
          </div>
          <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="phone"> 餐點價錢 </label> -->
            <label class="mb-2 block font-bold text-gray-700" for="phone"> 餐點價錢 </label>
            <input
              v-model="mealInfo.price"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              id="phone"
              type="number"
              min="0"
              placeholder="輸入餐點價錢(必填)"
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
            <label class="mb-2 block font-bold text-gray-700" for="message"> 單點 </label>
            <select v-model="mealInfo.combo" class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              >
              <option v-for="option in options" v-bind:value="option.value">
                {{ option.text }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label class="mb-2 block font-bold text-gray-700" for="message"> 照片 </label>
            <input type="file" id="input" @change="handleFiles" accept="image/png, image/gif, image/jpeg" />
          </div>
          
          <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="message"> 餐點描述 </label> -->
            <label class="mb-2 block font-bold text-gray-700" for="message"> 餐點描述 </label>
            <textarea
              v-model="mealInfo.description"
              class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
              id="message"
              rows="4"
              placeholder="餐點描述資訊"

            ></textarea>
          </div>
          <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="phone"> 餐點價錢 </label> -->
            <label class="mb-2 block text-red-600 text-center" v-if="checkHasUpload == true"> 有空白處尚未填寫或照片還沒有上傳 </label>
          </div>
          <div class="space-y-2">
            <div aria-hidden="true" class="border-t px-2 dark:border-gray-700"></div>

            <div class="px-6 py-2">
              <div class="grid grid-cols-[repeat(auto-fit,minmax(0,1fr))] gap-2">
                <button
                  @click="$emit('close')"
                  class="focus:ring-primary-600 focus:text-primary-600 dark:focus:border-primary-400 inline-flex min-h-[2.25rem] items-center justify-center gap-1 rounded-lg border border-gray-300 bg-white px-4 py-1 text-sm font-medium text-gray-800 outline-none transition-colors focus:border-blue-600 focus:bg-blue-50 focus:ring-2 focus:ring-inset focus:ring-offset-2 dark:focus:text-blue-400"
                >
                  <span class="flex items-center gap-1">
                    <span class=""> Cancel </span>
                  </span>
                </button>

                <button
                  @click="$emit('subm')"
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
        <!-- </div> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRestaurantStore } from '@/store/restaurant'
import { storeToRefs } from 'pinia'
const useRestaurant = useRestaurantStore()
const { mealInfo, checkHasUpload } = storeToRefs(useRestaurant)

const options = ref([
  { text: '單點', value: 0 },
  { text: '套餐', value: 1 },
])

const handleFiles = async (e: any) => {
  mealInfo.value.picture = e.target.files[0]
}
</script>

<style></style>
