<template>
  <div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <div class="fixed inset-0 bg-gray-100 bg-opacity-75 transition-opacity"></div>

    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="mx-auto mt-20 max-w-xl overflow-hidden rounded-2xl bg-white shadow-lg">
        <div class="px-6 py-4 text-center text-2xl font-bold uppercase text-gray-600">餐點內容</div>
        <div class="px-6 py-4">
          <div class="mb-4 flex flex-row items-center justify-between" v-for="(meal, index) in props.dishes">
            <div class="flex w-2/5 flex-row items-center">
              <!-- <img :src="'/api' + meal.picture" class="h-10 w-10 rounded-md object-cover" alt="test" /> -->
              <span class="ml-4 text-sm font-semibold">{{ meal.dish_name }}</span>
            </div>
            <div class="flex w-32 justify-between">
              <span class="select-none px-3 py-1 font-semibold">{{ meal.number }}</span>
            </div>
            <div class="w-16 text-center text-lg font-semibold">${{ meal.price * meal.number }}</div>
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
                  @click="$emit('close')"
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

const props = defineProps<{
    dishes: { dish_id: number, dish_name: string, number: number, price: number, rating: number }[]
}>()

console.log(props.dishes)

// const useRestaurant = useRestaurantStore()
// const { restaurantInfo } = storeToRefs(useRestaurant)
// const userOrder = ref([
//   {
//     name: 'test',
//     price: 100,
//     number: 1,
//     picture: '/api/test.jpg'
//   }
// ])
// const showTime = () => {
//   console.log(restaurantInfo.value)
// }
</script>

<style></style>
