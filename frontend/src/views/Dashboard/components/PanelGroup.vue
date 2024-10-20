<script setup lang="ts">
import { ElRow, ElCol, ElCard, ElSkeleton } from 'element-plus'
import { CountTo } from '@/components/CountTo'
import { useDesign } from '@/hooks/web/useDesign'
import { useI18n } from '@/hooks/web/useI18n'
import { ref, reactive, onMounted } from 'vue'
import userInfoService from '@/api/userInfo/userInfoService'
import { useUserStore } from '@/store/modules/user'
const { t } = useI18n()

const { getPrefixCls } = useDesign()

const prefixCls = getPrefixCls('panel')

const loading = ref(false)

const userStore = useUserStore()
const TSMCPoint = ref(500)

const totalState = reactive<AnalysisTotalTypes>({
  users: 0,
  messages: 0,
  moneys: 0,
  shoppings: 0
})

onMounted(async () => {
  const useraccount = userStore.getUserInfo
  if (useraccount) {
    const userInformation = await userInfoService.userInfoApi(useraccount.username)
    userStore.setUserAllInfomation(userInformation)
    TSMCPoint.value = userInformation.points
  }
})
</script>

<template></template>
