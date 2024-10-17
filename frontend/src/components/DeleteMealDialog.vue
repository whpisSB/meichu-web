<template>
  <div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <div class="fixed inset-0 bg-gray-50 bg-opacity-75 transition-opacity"></div>


    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="mx-auto mt-20 max-w-xl overflow-hidden rounded-2xl bg-white shadow-lg">
        <div class="bg-orange-300 px-6 py-4 text-center text-2xl font-bold uppercase text-gray-700"> 移除餐點 </div>
        <div class="px-6 py-4">
          <div class="mb-4 text-center">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="name"> 餐點名稱 </label> -->

            <i class="bx bx-error text-centerr text-7xl text-red-600">&#9888;</i>
            <label class="mb-2 block font-bold text-2xl text-black-700" for="name"> 確定移除餐點 </label>
          </div>
      
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

</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRestaurantStore } from '@/store/restaurant'
const editMealDialog = ref(false)
const useRestaurant = useRestaurantStore()
const { mealPrice } = storeToRefs(useRestaurant)
</script>

<style></style>
