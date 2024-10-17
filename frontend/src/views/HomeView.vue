<template>
  <div class="font-[sans-serif] text-[#333]">
    <div class="fle-col flex min-h-screen items-center justify-center px-4 py-6">
      <div class="grid w-full max-w-7xl items-center gap-4 md:grid-cols-2">
        <div
          class="max-w-md rounded-md border border-gray-300 bg-slate-50 p-6 shadow-[0_2px_22px_-4px_rgba(93,96,127,0.2)] max-md:mx-auto"
        >
          <form class="space-y-6">
            <div class="mb-10">
              <h3 class="text-3xl font-extrabold">Sign in</h3>
              <p class="mt-4 text-sm">
                Sign in to your account and explore a world of possibilities. Your journey begins here.
              </p>
            </div>
            <div>
              <label class="mb-2 block text-sm">User Account</label>
              <div class="relative flex items-center">
                <input
                  v-model="userInput.account"
                  name="username"
                  type="text"
                  required
                  class="w-full rounded-md border border-gray-300 px-4 py-3 text-sm outline-[#333]"
                  placeholder="Enter user name"
                />
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="#bbb"
                  stroke="#bbb"
                  class="absolute right-4 h-[18px] w-[18px]"
                  viewBox="0 0 24 24"
                >
                  <circle cx="10" cy="7" r="6" data-original="#000000"></circle>
                  <path
                    d="M14 15H6a5 5 0 0 0-5 5 3 3 0 0 0 3 3h12a3 3 0 0 0 3-3 5 5 0 0 0-5-5zm8-4h-2.59l.3-.29a1 1 0 0 0-1.42-1.42l-2 2a1 1 0 0 0 0 1.42l2 2a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42l-.3-.29H22a1 1 0 0 0 0-2z"
                    data-original="#000000"
                  ></path>
                </svg>
              </div>
            </div>
            <div>
              <label class="mb-2 block text-sm">Password</label>
              <div class="relative flex items-center">
                <input
                  v-model="userInput.password"
                  name="password"
                  type="password"
                  required
                  class="w-full rounded-md border border-gray-300 px-4 py-3 text-sm outline-[#333]"
                  placeholder="Enter password"
                />
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="#bbb"
                  stroke="#bbb"
                  class="absolute right-4 h-[18px] w-[18px] cursor-pointer"
                  viewBox="0 0 128 128"
                >
                  <path
                    d="M64 104C22.127 104 1.367 67.496.504 65.943a4 4 0 0 1 0-3.887C1.367 60.504 22.127 24 64 24s62.633 36.504 63.496 38.057a4 4 0 0 1 0 3.887C126.633 67.496 105.873 104 64 104zM8.707 63.994C13.465 71.205 32.146 96 64 96c31.955 0 50.553-24.775 55.293-31.994C114.535 56.795 95.854 32 64 32 32.045 32 13.447 56.775 8.707 63.994zM64 88c-13.234 0-24-10.766-24-24s10.766-24 24-24 24 10.766 24 24-10.766 24-24 24zm0-40c-8.822 0-16 7.178-16 16s7.178 16 16 16 16-7.178 16-16-7.178-16-16-16z"
                    data-original="#000000"
                  ></path>
                </svg>
              </div>
            </div>
            <div v-if="loginStatus != 0" class="mb-2 text-red-500">Account doesn't exist or wrong password</div>
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  class="h-4 w-4 shrink-0 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label for="remember-me" class="ml-3 block text-sm"> Remember me </label>
              </div>
            </div>
            <div class="!mt-10">
              <button
                @click="submit()"
                type="button"
                class="w-full rounded bg-[#333] px-4 py-2.5 text-sm font-semibold text-white shadow-xl hover:bg-black focus:outline-none"
              >
                Log in
              </button>
            </div>
            <p class="!mt-10 text-center text-sm">
              Forgot your password?<a
                href="javascript:void(0);"
                class="ml-1 whitespace-nowrap text-blue-600 hover:underline"
              >
                Click here</a
              >
            </p>
          </form>
        </div>
        <div class="max-md:mt-10">
          <img
            src="@/assets/taiwan-semiconductor-manufacturing-company-logo-svg.svg"
            class="h-full w-full object-cover"
            alt="Dining Experience"
          />
          <h1 class="mb-2 text-center text-4xl font-semibold">Welcome to TSMC Meal Provider</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import router from '@/router/index'
import { useUserStore } from '@/store/user'
import userService from '@/service/userService'

const userStore = useUserStore()
const loginStatus = ref(0)
const userInput = reactive({
  account: '',
  password: ''
})

const submit = async () => {
  const userInfo = await userService.userLogin(userInput.account, userInput.password)
  console.log(userInfo)
  if (userInfo.user_identity === 'invalid_user') {
    loginStatus.value = 1
  } else if (userInfo.user_identity === 'restaurant') {
    userStore.setUserInfo(userInfo)
    loginStatus.value = 0
    router.push({ path: '/restaurant' })
  } else if (userInfo.user_identity === 'admin') {
    userStore.setUserInfo(userInfo)
    loginStatus.value = 0
    router.push({ path: '/admin' })
  } else if (userInfo.user_identity === 'worker') {
    userStore.setUserInfo(userInfo)
    loginStatus.value = 0
    router.push({ path: '/worker' })
  }
}
</script>

<style>
body {
  background-image: url('@/assets/unsplash_-YHSwy6uqvk.png');
}
</style>
