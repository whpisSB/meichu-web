import type { user } from '../types/user'
import { useUserStore } from '@/store/user'

export default class userService {
  static async userLogin(user_account: string, user_password: string): Promise<user> {
    console.log(user_account, user_password)
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_account: user_account, user_password: user_password })
    })
    const result = await response.json()
    console.log(result)
    return result
  }
  static async userLogout(): Promise<void> {
    useUserStore().reset()
  }
  static async userCheckOuth(): Promise<boolean> {
    if (useUserStore().$state.userInfo.outh_token !== '') {
      return true
    } else {
      return false
    }
  }
}
