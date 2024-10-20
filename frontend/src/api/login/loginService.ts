import type { UserLoginType } from './types.ts'

export default class loginService {
  static async loginApi(userInfo: UserLoginType): Promise<any> {
    console.log(userInfo)
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userInfo)
    })
    console.log(await response.json())
    if (response.status != 200) {
      return false
    } else {
      return true
    }
  }
}
