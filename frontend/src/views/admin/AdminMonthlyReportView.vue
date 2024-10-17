<template>
  <WarningDialog v-if="showWarningDialog" message="你已經登出"></WarningDialog>
  
  <div class="mx-auto bg-white">
    <div class="flex flex-col-reverse lg:flex-row">
      <AdminSidebar class="min-h-screen w-full shadow-lg lg:w-1/6"></AdminSidebar>
      <div class="bg-white-100 lg:w-6/6 min-h-screen w-full">
        <!-- header -->
        <div class="mt-5 flex flex-row items-center justify-center px-5">
          <div class="text-gray-800">
            <div class="text-3xl font-bold">報表下載</div>
          </div>
        </div>
        <div class="mt-40 items-center justify-center sm:flex">
          <div class = "items-center">
            <form class="space-y-6 ">
              <div>
                <label class="mb-2 block text-sm">年分</label>
                <div class="relative flex items-center">
                  <input
                    v-model="submitData.year"
                    name="username"
                    type="number"
                    required
                    class="w-full rounded-md border border-gray-300 px-4 py-3 text-sm outline-[#333]"
                    placeholder="2003"
                    min=2000
                    max=2024
                  />
                </div>
              </div>
              <div>
                <label class="mb-2 block text-sm">月份</label>
                <div class="relative flex items-center">
                  <input
                    v-model="submitData.month"
                    type="number"
                    name="password"
                    required
                    class="w-full rounded-md border border-gray-300 px-4 py-3 text-sm outline-[#333]"
                    placeholder="20"
                    min=1
                    max=12
                  />
                </div>
              </div>
              <div class="!mt-10">
                <button
                  type="button"
                  @click="submit"
                  class="w-full rounded bg-[#333] px-4 py-2.5 text-sm font-semibold text-white shadow-xl hover:bg-black focus:outline-none"
                >
                  下載報表
                </button>
              </div>
            </form>
          </div>
        </div>
        <!-- end categories -->
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router'
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import workerService from '@/service/workerService'
import userService from '@/service/userService'
import adminService from '@/service/adminService'
import { useUserStore } from '@/store/user'
import type { restaurant, meal } from '@/types/worker'
import router from '@/router'

const userStore = useUserStore()
const { userInfo } = storeToRefs(userStore)

const showWarningDialog = ref(false)
const timer = ref()
const submitData = reactive({
  month: 6,
  year: 2024,
})

const submit = async () => {
  if (submitData.month < 1 || submitData.month > 12) {
    alert('月份請輸入1~12')
    return
  }
  if (submitData.year < 2000 || submitData.year > 2024) {
    alert('年分請輸入2000~2024')
    return
  }
  await downloadMonthlyReport()
}

const downloadMonthlyReport = async () => {
  const blob = await adminService.downloadMonthlyReport(userInfo.value.outh_token, submitData.year, submitData.month)
  if (!blob) {
    alert('下載失敗')
    return
  }
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  var fileName = 'monthly-report-' + submitData.year.toString()
  if (submitData.month < 10) {
    fileName += '-0'
    fileName += submitData.month.toString() + '.csv'
  } else {
    fileName += '-'
    fileName += submitData.month.toString() + '.csv'
  }
  link.setAttribute('download', fileName)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
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


<style>
</style>