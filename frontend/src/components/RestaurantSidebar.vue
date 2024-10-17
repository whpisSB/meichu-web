<template>
  <div
    class="shadow-blue-gray-900/5 relative w-full max-w-[20rem] flex-col rounded-xl bg-amber-100 bg-opacity-30 bg-clip-border p-4 text-gray-700 shadow-xl"
  >
    <nav class="text-blue-gray-700 flex max-w-[16rem] flex-col gap-1 p-2 font-sans text-base font-normal">
      <router-link
        to="/restaurant"
        class="hover:text-blue-gray-900 hove:border focus:bg-blue-gray-50 focus:text-blue-gray-900 active:bg-blue-gray-50 active:text-blue-gray-900 flex w-full items-center rounded-lg p-3 text-start leading-tight outline-none transition-all hover:bg-slate-300 hover:bg-opacity-80 focus:bg-opacity-80 active:bg-opacity-100"
      >
        <div class="mr-4 grid place-items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
            class="h-5 w-5"
          >
            <path
              fill-rule="evenodd"
              d="M2.25 2.25a.75.75 0 000 1.5H3v10.5a3 3 0 003 3h1.21l-1.172 3.513a.75.75 0 001.424.474l.329-.987h8.418l.33.987a.75.75 0 001.422-.474l-1.17-3.513H18a3 3 0 003-3V3.75h.75a.75.75 0 000-1.5H2.25zm6.04 16.5l.5-1.5h6.42l.5 1.5H8.29zm7.46-12a.75.75 0 00-1.5 0v6a.75.75 0 001.5 0v-6zm-3 2.25a.75.75 0 00-1.5 0v3.75a.75.75 0 001.5 0V9zm-3 2.25a.75.75 0 00-1.5 0v1.5a.75.75 0 001.5 0v-1.5z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </div>
        Menu
      </router-link>
      <router-link
        to="/restaurant/history-order"
        role="button"
        class="hover:bg-blue-gray-50 hover:text-blue-gray-900 focus:bg-blue-gray-50 focus:text-blue-gray-900 active:bg-blue-gray-50 active:text-blue-gray-900 flex w-full items-center rounded-lg p-3 text-start leading-tight outline-none transition-all hover:bg-gray-100 hover:bg-opacity-80 focus:bg-opacity-80 active:bg-opacity-80"
      >
        <div class="mr-4 grid place-items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
            class="h-5 w-5"
          >
            <path
              fill-rule="evenodd"
              d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 004.25 22.5h15.5a1.875 1.875 0 001.865-2.071l-1.263-12a1.875 1.875 0 00-1.865-1.679H16.5V6a4.5 4.5 0 10-9 0zM12 3a3 3 0 00-3 3v.75h6V6a3 3 0 00-3-3zm-3 8.25a3 3 0 106 0v-.75a.75.75 0 011.5 0v.75a4.5 4.5 0 11-9 0v-.75a.75.75 0 011.5 0v.75z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </div>
        訂單
      </router-link>
      <div
        role="button"
        @click="logout"
        class="hover:text-blue-gray-900 focus:bg-blue-gray-50 focus:text-blue-gray-900 active:bg-blue-gray-50 active:text-blue-gray-900 flex w-full rounded-lg p-3 text-start leading-tight outline-none transition-all hover:bg-gray-100 hover:bg-opacity-80 focus:bg-opacity-80 active:bg-opacity-80"
      >
        <div class="mr-4 grid">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
            class="h-5 w-5"
          >
            <path
              fill-rule="evenodd"
              d="M12 2.25a.75.75 0 01.75.75v9a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM6.166 5.106a.75.75 0 010 1.06 8.25 8.25 0 1011.668 0 .75.75 0 111.06-1.06c3.808 3.807 3.808 9.98 0 13.788-3.807 3.808-9.98 3.808-13.788 0-3.808-3.807-3.808-9.98 0-13.788a.75.75 0 011.06 0z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </div>
        Log Out
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import router from '@/router/index'
import userService from '@/service/userService'

const logout = () => {
  userService.userLogout()
}
</script>

<style></style>
