import type { rewardItemType } from './types'

export default class rewardService {
  static async getRewardApi(): Promise<rewardItemType[]> {
    const response = await fetch('/api/reward')
    const data = await response.json()
    return data
  }
  static async exchangeRewardApi(line_id: string, reward_id: string): Promise<any> {
    console.log(line_id, reward_id)
    const response = await fetch('/api/exchange_reward', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ line_id: line_id, reward_id: reward_id })
    })
    console.log(response)
    const data = await response.json()
    console.log(data)
    return data
  }
}
