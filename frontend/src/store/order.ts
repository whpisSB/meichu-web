import { defineStore } from 'pinia'
import { type user } from '@/types/user'
import { type order } from '@/types/worker'

export const useOrderStore = defineStore({
  id: 'userOrder',
  state: () => ({
    orders: [] as order[],
    selectIndex: 0,
    overAllRating: 0
  }),
  persist: true,
  actions: {
    setSelectIndex(index: number) {
      this.selectIndex = index
    }
  }
})
