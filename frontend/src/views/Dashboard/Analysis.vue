<script setup lang="ts">
import PanelGroup from './components/PanelGroup.vue'
import { ElRow, ElCol, ElCard, ElSkeleton } from 'element-plus'
import { Echart } from '@/components/Echart'
import { pieOptions, barOptions, lineOptions } from './echarts-data'
import { ref, reactive } from 'vue'
import { set } from 'lodash-es'
import { EChartsOption } from 'echarts'
import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

const loading = ref(true)

//const pieOptionsData = reactive<EChartsOption>(pieOptions) as EChartsOption

// 用户来源
// const getUserAccessSource = async () => {
//   const res = await getUserAccessSourceApi().catch(() => {})
//   if (res) {
//     set(
//       pieOptionsData,
//       'legend.data',
//       res.data.map((v) => t(v.name))
//     )
//     pieOptionsData!.series![0].data = res.data.map((v) => {
//       return {
//         name: t(v.name),
//         value: v.value
//       }
//     })
//   }
// }

const barOptionsData = reactive<EChartsOption>(barOptions) as EChartsOption

// 周活跃量
const getWeeklyUserActivity = () => {
  const res = [
    { value: 4, name: 'analysis.monday' },
    { value: 2, name: 'analysis.tuesday' },
    { value: 5, name: 'analysis.wednesday' },
    { value: 2, name: 'analysis.thursday' },
    { value: 9, name: 'analysis.friday' },
    { value: 0, name: 'analysis.saturday' },
    { value: 0, name: 'analysis.sunday' }
  ]

  set(
    barOptionsData,
    'xAxis.data',
    res.map((v) => t(v.name))
  )
  set(barOptionsData, 'series', [
    {
      name: t('analysis.activeQuantity'),
      data: res.map((v) => v.value),
      type: 'bar'
    }
  ])
}

const lineOptionsData = reactive<EChartsOption>(lineOptions) as EChartsOption

// 每月销售总额
const getMonthlySales = async () => {
  const res = [
    { actual: 120, name: 'analysis.january' },
    { actual: 82, name: 'analysis.february' },
    { actual: 91, name: 'analysis.march' },
    { actual: 154, name: 'analysis.april' },
    { actual: 162, name: 'analysis.may' },
    { actual: 140, name: 'analysis.june' },
    { actual: 145, name: 'analysis.july' },
    { actual: 250, name: 'analysis.august' },
    { actual: 134, name: 'analysis.september' },
    { actual: 56, name: 'analysis.october' },
    { actual: 99, name: 'analysis.november' },
    { actual: 123, name: 'analysis.december' }
  ]
  set(
    lineOptionsData,
    'xAxis.data',
    res.map((v) => t(v.name))
  )
  set(lineOptionsData, 'series', [
    // {
    //   name: t('analysis.estimate'),
    //   smooth: true,
    //   type: 'line',
    //   data: res.map((v) => v.estimate),
    //   animationDuration: 2800,
    //   animationEasing: 'cubicInOut'
    // },
    {
      name: t('analysis.actual'),
      smooth: true,
      type: 'line',
      itemStyle: {},
      data: res.map((v) => v.actual),
      animationDuration: 2800,
      animationEasing: 'quadraticOut'
    }
  ])
}

const getAllApi = async () => {
  getWeeklyUserActivity()
  getMonthlySales()
  loading.value = false
}

getAllApi()
</script>

<template>
  <PanelGroup />
  <ElRow :gutter="20" justify="space-between">
    <ElCol>
      <ElCard shadow="hover" class="mb-20px">
        <ElSkeleton :loading="loading" animated>
          <Echart :options="barOptionsData" :height="300" />
        </ElSkeleton>
      </ElCard>
    </ElCol>
    <ElCol>
      <ElCard shadow="hover" class="mb-20px">
        <ElSkeleton :loading="loading" animated>
          <Echart :options="lineOptionsData" :height="350" />
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
