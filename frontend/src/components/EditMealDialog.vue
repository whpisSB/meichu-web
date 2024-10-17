<template>
<div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <div class="fixed inset-0 bg-gray-50 bg-opacity-75 transition-opacity"></div>


    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
    <div class="mx-auto mt-20 max-w-xl overflow-hidden rounded-2xl bg-gray-50 shadow-lg">
        <div class="bg-orange-300 px-6 py-4 text-center text-2xl font-bold uppercase text-gray-700">修改餐點價格</div>
        <div class="px-6 py-4">
        
        <div class="mb-4">
            <!-- <label class="mb-2 block font-bold text-gray-700" for="phone"> 餐點價錢 </label> -->
            <label class="mb-2 block font-bold text-gray-700" for="phone"> 修改價錢 </label>
            <input
                v-model="mealPrice.updated_price"
                class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
                id="phone"
                type="number"
                min="0"
                placeholder="輸入修改價錢(必填)"

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
                @click="$emit('sub')"
                class="inline-flex min-h-[2.25rem] items-center justify-center gap-1 rounded-lg border border-transparent bg-green-600 px-4 py-1 text-sm font-medium text-white shadow outline-none transition-colors hover:bg-green-500 focus:bg-green-700 focus:ring-2 focus:ring-inset focus:ring-white focus:ring-offset-2 focus:ring-offset-green-700 "
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
import { storeToRefs } from 'pinia'
import { useRestaurantStore } from '@/store/restaurant'
const editMealDialog = ref(false)
const useRestaurant = useRestaurantStore()
const { mealPrice } = storeToRefs(useRestaurant)
const mealInfo = ref<any>({})
</script>

<style></style>
