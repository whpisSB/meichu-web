import { defineStore } from 'pinia'
import { type user } from '@/types/user'

export const useUserStore = defineStore({
  id: 'userInfomation',
  state: () => ({
    userInfo: {
      outh_token: '',
      user_identity: '',
      restaurant_id: '',
      notify: false
    } as user
  }),
  persist: true,
  actions: {
    setUserInfo(user: user) {
      this.userInfo = user
    },
    reset() {
      this.userInfo = {
        outh_token: '',
        user_identity: '',
        restaurant_id: ''
      } as user
    }
  }
})
