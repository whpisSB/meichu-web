import type { rewardItemType } from './types'

export default class rewardService {
  static async getRewardApi(): Promise<rewardItemType[]> {
    const response = await fetch('/api/reward')
    const data = await response.json()
    return data
  }
}
