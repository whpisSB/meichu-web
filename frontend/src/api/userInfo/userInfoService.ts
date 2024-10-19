export default class userInfoService {
  static async userInfoApi(email: string): Promise<any> {
    const url = `/api/user_info`
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // Set the Content-Type header
      },
      body: JSON.stringify({
        email: email
      })
    })
    return await response.json()
  }
}
