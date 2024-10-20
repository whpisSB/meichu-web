<script setup lang="ts">
import { useTimeAgo } from '@/hooks/web/useTimeAgo'
import { ElRow, ElCol, ElSkeleton, ElCard, ElDivider, ElLink } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { ref, reactive, onMounted } from 'vue'
import { CountTo } from '@/components/CountTo'
import { formatTime } from '@/utils'
import { EChartsOption } from 'echarts'
import { radarOption } from './echarts-data'
import { Highlight } from '@/components/Highlight'
import userInfoService from '@/api/userInfo/userInfoService'
import { useUserStore } from '@/store/modules/user'
// import { getProjectApi, getDynamicApi, getTeamApi, getRadarApi } from '@/api/dashboard/workplace'
import type { WorkplaceTotal, Project, Dynamic, Team } from '@/api/dashboard/workplace/types'
import { set } from 'lodash-es'

const loading = ref(true)
const TSMCPoint = ref(500)
const userStore = useUserStore()
const totalSate = reactive<WorkplaceTotal>({
  project: 10,
  access: 10,
  todo: 10
})



onMounted(async () => {
  const useraccount = userStore.getUserInfo
  if (useraccount) {
    const userInformation = await userInfoService.userInfoApi(useraccount.username)
    TSMCPoint.value = userInformation.points
  }
})
const projects = reactive<Project[]>([])

// 获取项目数

// 获取动态

const dynamics = reactive<Dynamic[]>([
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  },
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  },
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  },
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  },
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  },
  {
    keys: ['workplace.push', 'Github'],
    time: new Date()
  }
])

// 获取团队
const team = reactive<Team[]>([])

// 获取指数
const radarOptionData = reactive<EChartsOption>(radarOption) as EChartsOption

const getRadar = () => {
  const res = [
    { name: 'workplace.quote', max: 65, personal: 42, team: 50 },
    { name: 'workplace.contribution', max: 160, personal: 30, team: 140 },
    { name: 'workplace.hot', max: 300, personal: 20, team: 28 },
    { name: 'workplace.yield', max: 130, personal: 35, team: 35 },
    { name: 'workplace.follow', max: 100, personal: 80, team: 90 }
  ]
  set(
    radarOptionData,
    'radar.indicator',
    res.map((v) => {
      return {
        name: 'test',
        max: v.max
      }
    })
  )
  set(radarOptionData, 'series', [
    {
      name: 'test',
      type: 'radar',
      data: [
        {
          value: res.map((v) => v.personal),
          name: 'test'
        },
        {
          value: res.map((v) => v.team),
          name: 'test'
        }
      ]
    }
  ])
}

const getAllApi = () => {
  getRadar()
  loading.value = false
}

getAllApi()

const { t } = useI18n()
</script>

<template>
  <div>
    <ElCard shadow="never">
      <ElSkeleton :loading="loading" animated>
        <ElRow :gutter="20" justify="space-between">
          <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
            <div class="flex items-center">
              <img
                src="@/assets/imgs/avatar.jpg"
                alt=""
                class="w-70px h-70px rounded-[50%] mr-20px"
              />
              <div>
                <div class="text-20px">
                  {{ t('workplace.goodMorning') }}，Archer，{{ t('workplace.happyDay') }}
                </div>
                <div class="mt-10px text-14px text-gray-500">
                  {{ t('workplace.toady') }}，20℃ - 32℃！
                </div>
              </div>
            </div>
          </ElCol>
          <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
            <div class="flex h-70px items-center justify-end lt-sm:mt-20px">
              <div class="px-8px text-right">
                <div class="text-14px text-gray-400 mb-20px">{{ t('workplace.project') }}</div>
                <CountTo
                  class="text-20px"
                  :start-val="0"
                  :end-val="totalSate.project"
                  :duration="2600"
                />
              </div>
              <ElDivider direction="vertical" />
              <div class="px-8px text-right">
                <div class="text-14px text-gray-400 mb-20px">{{ t('workplace.toDo') }}</div>
                <CountTo
                  class="text-20px"
                  :start-val="0"
                  :end-val="totalSate.todo"
                  :duration="2600"
                />
              </div>
              <ElDivider direction="vertical" border-style="dashed" />
              <div class="px-8px text-right">
                <div class="text-14px text-gray-400 mb-20px">{{ t('workplace.access') }}</div>
                <CountTo
                  class="text-20px"
                  :start-val="0"
                  :end-val="totalSate.access"
                  :duration="2600"
                />
              </div>
            </div>
          </ElCol>
        </ElRow>
      </ElSkeleton>
    </ElCard>
  </div>

  <ElRow class="mt-20px" :gutter="20" justify="space-between">
    <ElCol :xl="16" :lg="16" :md="24" :sm="24" :xs="24" class="mb-20px">
      <ElCard shadow="never">
        <template #header>
          <div class="flex justify-between">
            <span>{{ t('workplace.project') }}</span>
            <ElLink type="primary" :underline="false">{{ t('workplace.more') }}</ElLink>
          </div>
        </template>
        <ElSkeleton :loading="loading" animated>
          <ElRow>
            <ElCol
              v-for="(item, index) in projects"
              :key="`card-${index}`"
              :xl="8"
              :lg="8"
              :md="12"
              :sm="24"
              :xs="24"
            >
              <ElCard shadow="hover">
                <div class="flex items-center">
                  <Icon :icon="item.icon" :size="25" class="mr-10px" />
                  <span class="text-16px">{{ item.name }}</span>
                </div>
                <div class="mt-15px text-14px text-gray-400">{{ t(item.message) }}</div>
                <div class="mt-20px text-12px text-gray-400 flex justify-between">
                  <span>{{ item.personal }}</span>
                  <span>{{ formatTime(item.time, 'yyyy-MM-dd') }}</span>
                </div>
              </ElCard>
            </ElCol>
          </ElRow>
        </ElSkeleton>
      </ElCard>

      <ElCard shadow="never" class="mt-20px">
        <template #header>
          <div class="flex justify-between">
            <span>{{ t('workplace.dynamic') }}</span>
            <ElLink type="primary" :underline="false">{{ t('workplace.more') }}</ElLink>
          </div>
        </template>
        <ElSkeleton :loading="loading" animated>
          <div v-for="(item, index) in dynamics" :key="`dynamics-${index}`">
            <div class="flex items-center">
              <img
                src="@/assets/imgs/avatar.jpg"
                alt=""
                class="w-35px h-35px rounded-[50%] mr-20px"
              />
              <div>
                <div class="text-14px">
                  <Highlight :keys="item.keys.map((v) => t(v))">
                    {{ t('workplace.pushCode') }}
                  </Highlight>
                </div>
                <div class="mt-15px text-12px text-gray-400">
                  {{ useTimeAgo(item.time) }}
                </div>
              </div>
            </div>
            <ElDivider />
          </div>
        </ElSkeleton>
      </ElCard>
    </ElCol>
    <ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
      <ElCard shadow="hover" class="mb-20px">
        <ElSkeleton :loading="loading" animated :rows="2">
          <template #default>
            <div :class="`${prefixCls}__item flex justify-between`">
              <div>
                <div
                  :class="`${prefixCls}__item--icon ${prefixCls}__item--peoples p-16px inline-block rounded-6px`"
                >
                  <Icon icon="svg-icon:shopping" :size="40" />
                </div>
              </div>
              <div class="flex flex-col justify-between">
                <div
                  :class="`${prefixCls}__item--text text-16px font-700 text-black-500 text-right`"
                  >{{ t('analysis.transactionAmount') }}</div
                >
                <CountTo
                  class="text-20px font-700 text-right"
                  :start-val="0"
                  :end-val="TSMCPoint"
                  :duration="1000"
                />
              </div>
            </div>
          </template>
        </ElSkeleton>
      </ElCard>

      <ElCard shadow="never" class="mt-20px">
        <template #header>
          <span>{{ t('workplace.team') }}</span>
        </template>
        <ElSkeleton :loading="loading" animated>
          <ElRow>
            <ElCol v-for="item in team" :key="`team-${item.name}`" :span="12" class="mb-20px">
              <div class="flex items-center">
                <Icon :icon="item.icon" class="mr-10px" />
                <ElLink type="default" :underline="false">
                  {{ item.name }}
                </ElLink>
              </div>
            </ElCol>
          </ElRow>
        </ElSkeleton>
      </ElCard>
    </ElCol>
  </ElRow>
</template>

<style lang="less" scoped>
@prefix-cls: ~'@{adminNamespace}-panel';

.@{prefix-cls} {
  &__item {
    &--peoples {
      color: #40c9c6;
    }

    &--message {
      color: #36a3f7;
    }

    &--money {
      color: #f4516c;
    }

    &--shopping {
      color: #34bfa3;
    }

    &:hover {
      :deep(.@{adminNamespace}-icon) {
        color: #fff !important;
      }
      .@{prefix-cls}__item--icon {
        transition: all 0.38s ease-out;
      }
      .@{prefix-cls}__item--peoples {
        background: #40c9c6;
      }
      .@{prefix-cls}__item--message {
        background: #36a3f7;
      }
      .@{prefix-cls}__item--money {
        background: #f4516c;
      }
      .@{prefix-cls}__item--shopping {
        background: #34bfa3;
      }
    }
  }
}
</style>
