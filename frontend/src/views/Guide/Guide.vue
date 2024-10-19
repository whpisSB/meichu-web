<script setup lang="tsx">
import { ref, reactive, unref } from 'vue'
import { ElLink, ElDivider, ElTag } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { BaseButton } from '@/components/Button'
import { useTable } from '@/hooks/web/useTable'
import { getCardTableListApi, getTreeTableListApi } from '@/api/table'

const { tableRegister, tableState } = useTable({
  fetchDataApi: async () => {
    const { currentPage, pageSize } = tableState
    const res = await getTreeTableListApi({
      pageIndex: unref(currentPage),
      pageSize: unref(pageSize)
    })
    return {
      list: res.data.list,
      total: res.data.total
    }
  }
})
const { dataList, total, currentPage, pageSize } = tableState

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
        <div>
          <div class="flex-1 text-center" @click="() => actionClick(item)">
            <ElLink :underline="false">加入購物車</ElLink>
          </div>
        </div>
      </template>
    </Table>
  </ContentWrap>
  <ContentWrap title="購物車清單">
    <Table
      v-model:pageSize="pageSize"
      v-model:currentPage="currentPage"
      :columns="columns"
      :data="dataList"
      row-key="id"
      :loading="loading"
      sortable
      :pagination="{
        total: total
      }"
      @register="tableRegister"
    />
  </ContentWrap>
</template>
