<script setup lang="tsx">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import { Table, TableColumn } from '@/components/Table'
import { ref, onMounted } from 'vue'
// import { ElTag } from 'element-plus'
// import { BaseButton } from '@/components/Button'

// interface Params {
//   pageIndex?: number
//   pageSize?: number
// }
interface RankingListProps {
  name: string
  github_id: string
  email: string
  line_id: string
  points: number
  total_points: number
  group: string
}

const rankingList = async (): Promise<RankingListProps[]> => {
  const response = await fetch('/api/all_users')
  return response.json()
}

interface ListProps {
  name: string
  email: string
  importance: number
  group: string
}

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

const loading = ref(true)
const List = ref<RankingListProps[]>([])
onMounted(async () => {
  const res = await rankingList()
  console.log(res)
  List.value = res.map(item => ({
    name: item.name,
    email: item.email,
    importance: item.total_points,
    group: item.group
  }))
  loading.value = false
})
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