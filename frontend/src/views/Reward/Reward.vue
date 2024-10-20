<script setup lang="tsx">
import { ref, reactive, unref, onMounted } from 'vue'
import { ElLink, ElDivider, ElTag, ElDialog, ElInput, ElButton, ElMessage } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { BaseButton } from '@/components/Button'
import rewardServce from '@/api/reward/rewardService'
import { useTable } from '@/hooks/web/useTable'
import { getTreeTableListApi } from '@/api/table'
import { rewardItemType } from '@/api/reward/types'
import { useUserStore } from '@/store/modules/user'

// const { tableRegister, tableState } = useTable({
//   fetchDataApi: async () => {
//     const { currentPage, pageSize } = tableState
//     const res = await getTreeTableListApi({
//       pageIndex: unref(currentPage),
//       pageSize: unref(pageSize)
//     })
//     return {
//       list: res.data.list,
//       total: res.data.total
//     }
//   }
// })
// const { dataList, total, currentPage, pageSize } = tableState

const { t } = useI18n()

const columns = reactive<TableColumn[]>([
  {
    field: 'selection',
    type: 'selection'
  },
  {
    field: 'index',
    label: t('tableDemo.index'),
    type: 'index'
  },
  {
    field: 'content',
    label: t('tableDemo.header'),
    children: [
      {
        field: 'title',
        label: t('tableDemo.title')
      },
      {
        field: 'author',
        label: t('tableDemo.author')
      },
      {
        field: 'display_time',
        label: t('tableDemo.displayTime')
      },
      {
        field: 'importance',
        label: t('tableDemo.importance'),
        formatter: (_: Recordable, __: TableColumn, cellValue: number) => {
          return (
            <ElTag type={cellValue === 1 ? 'success' : cellValue === 2 ? 'warning' : 'danger'}>
              {cellValue === 1
                ? t('tableDemo.important')
                : cellValue === 2
                  ? t('tableDemo.good')
                  : t('tableDemo.commonly')}
            </ElTag>
          )
        }
      },
      {
        field: 'pageviews',
        label: t('tableDemo.pageviews')
      }
    ]
  },
  {
    field: 'action',
    label: t('tableDemo.action'),
    slots: {
      default: (data) => {
        return (
          <BaseButton type="primary" onClick={() => actionFn(data)}>
            {t('tableDemo.action')}
          </BaseButton>
        )
      }
    }
  }
])

const actionFn = (data) => {
  console.log(data)
}

interface Params {
  pageIndex?: number
  pageSize?: number
}

const loading = ref(false)
const tableDataList = ref<rewardItemType[]>([])
const selectedItem = ref<rewardItemType>({
  description: '',
  points: 0,
  reward_id: 0,
  thumbnail_image: '',
  title: ''
})
onMounted(async () => {
  console.log('onMounted')
  tableDataList.value = await rewardServce.getRewardApi()
})
// const tableDataList = ref<any[]>([
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png',
//     name: 'Alipay',
//     desc: '餅乾'
//   },
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png',
//     name: 'Angular',
//     desc: '飲料'
//   },
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png',
//     name: 'Bootstrap',
//     desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
//   },
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png',
//     name: 'React',
//     desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
//   },
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png',
//     name: 'Vue',
//     desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
//   },
//   {
//     logo: 'https://gw.alipayobjects.com/zos/rmsportal/nxkuOJlFJuAUhzlMTCEe.png',
//     name: 'Webpack',
//     desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
//   }
// ])

const actionClick = (item: rewardItemType) => {
  selectedItem.value = item
  dialogVisible.value = true
}

const handleConfirm = async () => {
  if (!selectedItem.value) return

  loading.value = true
  try {
    const userAllInfomation = userStore.userAllInfomation
    const response = await rewardServce.exchangeRewardApi(
      userAllInfomation.line_id,
      selectedItem.value.reward_id.toString()
    )
    console.log(response)
    if (response) {
      ElMessage.success('兌換成功！')
      // Update the user's points
      // const userInfo = userStore.getUserInfo()
      // if (userInfo) {
      //   userStore.setUserInfo({
      //     ...userInfo,
      //     points: userInfo.points - selectedItem.value.points
      //   })
      // }
      // Refresh the rewards list
    } else {
      ElMessage.error(response.message || '兌換失敗，請稍後再試。')
    }
  } catch (error) {
    console.error('Error exchanging reward:', error)
    ElMessage.error('兌換時發生錯誤，請稍後再試。')
  } finally {
    loading.value = false
    dialogVisible.value = false
  }
}

// Add these new refs
const dialogVisible = ref(false)
const quantity = ref(1)
const userStore = useUserStore()
</script>

<template>
  <ContentWrap title="商品清單">
    <Table
      :columns="columns"
      :data="tableDataList"
      :loading="loading"
      custom-content
      :card-wrap-style="{
        width: '300px',
        marginBottom: '20px',
        marginRight: '20px'
      }"
    >
      <template #content="row">
        <div class="flex flex-col cursor-pointer">
          <div class="flex justify-between mb-2">
            <div class="font-bold text-lg">{{ row.title }}</div>
            <div class="font-bold text-lg text-green-600">{{ row.points }}P</div>
          </div>
          <div class="flex justify-center mb-2">
            <img :src="row.thumbnail_image" class="w-48 h-48 object-cover rounded" alt="" />
          </div>
          <div class="text-sm mb-2">{{ row.description }}</div>
        </div>
      </template>
      <template #content-footer="item">
        <div>
          <div class="flex-1 text-center" @click="() => actionClick(item)">
            <ElLink :underline="false">加入購物車</ElLink>
          </div>
        </div>
      </template>
    </Table>
  </ContentWrap>

  <!-- Add this dialog component -->
  <ElDialog v-model="dialogVisible" title="確認購買" width="30%">
    <div v-if="selectedItem">
      <p>{{ selectedItem.title }}</p>
      <p>價格: {{ selectedItem.points }}P</p>
      <p>數量: 1</p>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="handleConfirm" :loading="loading">確認兌換</ElButton>
      </span>
    </template>
  </ElDialog>
</template>
