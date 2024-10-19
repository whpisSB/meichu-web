<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { Table } from '@/components/Table'
import { getCardTableListApi } from '@/api/table'
import { ref } from 'vue'
import { ElLink, ElDivider } from 'element-plus'

interface Params {
  pageIndex?: number
  pageSize?: number
}

const loading = ref(true)

const tableDataList = ref<any[]>([])

const getTableList = async (params?: Params) => {
  const res = await getCardTableListApi(
    params || {
      pageIndex: 1,
      pageSize: 10
    }
  )
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
  if (res) {
    tableDataList.value = res.data.list
  }
  tableDataList.value = [
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png',
      name: 'Alipay',
      desc: '餅乾'
    },
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png',
      name: 'Angular',
      desc: '飲料'
    },
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png',
      name: 'Bootstrap',
      desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
    },
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png',
      name: 'React',
      desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
    },
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png',
      name: 'Vue',
      desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
    },
    {
      logo: 'https://gw.alipayobjects.com/zos/rmsportal/nxkuOJlFJuAUhzlMTCEe.png',
      name: 'Webpack',
      desc: '在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。'
    }
  ]
}

getTableList()

const actionClick = (row?: any) => {
  console.log(row)
}
</script>

<template>
  <ContentWrap title="商品清單">
    <!-- <ContentWrap :title="t('tableDemo.cardTable')"> -->
    <Table
      :columns="[]"
      :data="tableDataList"
      :loading="loading"
      custom-content
      :card-wrap-style="{
        width: '400px',
        marginBottom: '20px',
        marginRight: '20px'
      }"
    >
      <template #content="row">
        <div class="flex cursor-pointer">
          <div class="pr-16px">
            <img :src="row.logo" class="w-48px h-48px rounded-[50%]" alt="" />
          </div>
          <div>
            <div class="mb-12px font-700 font-size-16px">{{ row.name }}</div>
            <div class="line-clamp-3 font-size-12px">{{ row.desc }}</div>
          </div>
        </div>
      </template>
      <template #content-footer="item">
        <div class="flex justify-center items-center">
          <div class="flex-1 text-center" @click="() => actionClick(item)">
            <ElLink :underline="false">操作一</ElLink>
          </div>
          <ElDivider direction="vertical" />
          <div class="flex-1 text-center" @click="() => actionClick(item)">
            <ElLink :underline="false">加入清單</ElLink>
          </div>
        </div>
      </template>
    </Table>
  </ContentWrap>
</template>
