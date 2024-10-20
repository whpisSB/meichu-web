<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ref } from 'vue'
// import { ElTag } from 'element-plus'
// import { BaseButton } from '@/components/Button'

// interface Params {
//   pageIndex?: number
//   pageSize?: number
// }

interface ListProps {
  name: string
  email: string
  importance: number
  group: string
}

const List: ListProps[] = []

for (let i = 0; i < 10; i++) {
  List.push({
    name: i.toString(),
    email: 'email',
    group: 'group',
    importance: i
  })
}
console.log(List)

const { t } = useI18n()

const columns: TableColumn[] = [
  {
    field: 'name',
    label: t('tableDemo.title')
  },
  {
    field: 'email',
    label: t('tableDemo.author')
  },
  {
    field: 'importance',
    label: t('tableDemo.importance'),
    sortable: true
  },
  {
    field: 'group',
    label: t('tableDemo.pageviews')
  }
]

const loading = ref(false)
// const actionFn = (data: any) => {
//   console.log(data)
// }
</script>

<template>
  <ContentWrap :title="t('tableDemo.table')" :message="t('tableDemo.tableDes')">
    <Table
      :columns="columns"
      :data="List"
      :loading="loading"
      :defaultSort="{ prop: 'display_time', order: 'descending' }"
    />
  </ContentWrap>
</template>