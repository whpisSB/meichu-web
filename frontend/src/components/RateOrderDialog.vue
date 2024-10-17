<template>
  <div id="modal" class="relative z-10" aria-labelledby="modal-title" role="dialog">
    <!--
        Background backdrop, show/hide based on modal state.
    
        Entering: "ease-out duration-300"
          From: "opacity-0"
          To: "opacity-100"
        Leaving: "ease-in duration-200"
          From: "opacity-100"
          To: "opacity-0"
      -->

    <div class="fixed inset-0 bg-gray-50 bg-opacity-75 transition-opacity"></div>

    <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <!--
            Modal panel, show/hide based on modal state.
    
            Entering: "ease-out duration-300"
              From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              To: "opacity-100 translate-y-0 sm:scale-100"
            Leaving: "ease-in duration-200"
              From: "opacity-100 translate-y-0 sm:scale-100"
              To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          -->

        <div
          class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg"
        >
          <!-- <div class="relative overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-500 rtl:text-right">
              <thead class="bg-gray-50 text-xs uppercase text-gray-700">
                <tr>
                  <th scope="col" class="px-6 py-3">Product name</th>
                  <th scope="col" class="px-6 py-3">Color</th>
                  <th scope="col" class="px-6 py-3">Category</th>
                  <th scope="col" class="px-6 py-3">Price</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b bg-white">
                  <th scope="row" class="whitespace-nowrap px-6 py-4 font-medium text-gray-900">
                    Apple MacBook Pro 17"
                  </th>
                  <td class="px-6 py-4">Silver</td>
                  <td class="px-6 py-4">Laptop</td>
                  <td class="px-6 py-4">$2999</td>
                </tr>
                <tr class="border-b bg-white">
                  <th scope="row" class="whitespace-nowrap px-6 py-4 font-medium text-gray-900">
                    Microsoft Surface Pro
                  </th>
                  <td class="px-6 py-4">White</td>
                  <td class="px-6 py-4">Laptop PC</td>
                  <td class="px-6 py-4">$1999</td>
                </tr>
                <tr class="bg-white">
                  <th scope="row" class="whitespace-nowrap px-6 py-4 font-medium text-gray-900">Magic Mouse 2</th>
                  <td class="px-6 py-4">Black</td>
                  <td class="px-6 py-4">Accessories</td>
                  <td class="px-6 py-4">$99</td>
                </tr>
              </tbody>
            </table>
          </div> -->

          <div class="relative rounded-lg bg-white p-5 text-center shadow sm:p-5">
            <div class="flex items-center justify-center text-center">
              請給這餐廳評分
              <svg
                style="cursor: pointer"
                @click="change(1)"
                class="ms-3 h-4 w-4 text-yellow-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-if="point >= 2"
                @click="change(2)"
                class="ms-3 h-4 w-4 text-yellow-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-else
                @click="change(2)"
                class="ms-3 h-4 w-4 text-gray-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-if="point >= 3"
                @click="change(3)"
                class="ms-3 h-4 w-4 text-yellow-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-else
                @click="change(3)"
                class="ms-3 h-4 w-4 text-gray-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-if="point >= 4"
                @click="change(4)"
                class="ms-3 h-4 w-4 text-yellow-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-else
                @click="change(4)"
                class="ms-3 h-4 w-4 text-gray-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-if="point >= 5"
                @click="change(5)"
                class="ms-3 h-4 w-4 text-yellow-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
              <svg
                style="cursor: pointer"
                v-else
                @click="change(5)"
                class="ms-3 h-4 w-4 text-gray-300"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 22 20"
              >
                <path
                  d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"
                />
              </svg>
            </div>
            <!-- <button
              type="button"
              class="absolute right-2.5 top-2.5 ml-auto inline-flex items-center rounded-lg bg-transparent p-1.5 text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900"
              data-modal-toggle="successModal"
            >
              <svg
                aria-hidden="true"
                class="h-5 w-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <span class="sr-only">Close modal</span>
            </button>
            <div class="mx-auto mb-3.5 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 p-2">
              <svg
                aria-hidden="true"
                class="h-8 w-8 text-green-500"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              <span class="sr-only">Success</span>
            </div> -->
            <button
              @click="$emit('close')"
              type="button"
              class="hover:bg-primary-700 mt-5 rounded-lg bg-blue-600 px-3 py-2 text-center text-sm font-medium text-white focus:outline-none focus:ring-4"
            >
              評分完成
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'
import { ref, computed, reactive, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
const orderStore = useOrderStore()
const userStore = useUserStore()
const { orders, selectIndex, overAllRating } = storeToRefs(orderStore)

const point = ref(5)
const change = (num: number) => {
  point.value = num
  overAllRating.value = num
  console.log(overAllRating.value)
}
</script>

<style></style>
