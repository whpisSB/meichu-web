import type { order, restaurant, orderReview } from '../types/worker'

export default class workerService {
  static async getRestaurantList(token: string): Promise<any[]> {
    try {
      const response = await fetch('/api/main/restaurant_list')
      const data = await response.json()
      for (let i = 0; i < data.restaurants.length; i++) {
        const respones2 = await this.getRestaurant(token, data.restaurants[i].id.toString())
        data.restaurants[i].open_time = respones2.open_time
        data.restaurants[i].close_time = respones2.close_time
      }
      return data.restaurants
    } catch (error) {
      console.error(`GET /api/main/restaurant_list ${error}`)
      throw error
    }
  }

  static async getRestaurant(token: string, restaurant_id: string): Promise<restaurant> {
    try {
      const response = await fetch('/api/main/restaurant/' + restaurant_id, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      if (response.status === 403) {
        throw new Error('Permission Denied')
      }
      const data = await response.json()
      return data
    } catch (error) {
      console.error(`GET /api/main/restaurant/${restaurant_id}`, error)
      throw error
    }
  }

  static async getHistoryOrder(token: string): Promise<order[]> {
    try {
      const response = await fetch('/api/main/history', {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      if (response.status === 403) {
        throw new Error('Permission Denied')
      }
      const data = await response.json()
      return data.orders
    } catch (error) {
      console.error(`GET /api/main/history`, error)
      throw error
    }
  }

  // rating order by user
  static async reviewOrder(token: string, order_id: number, overAllRating: number, order: order): Promise<boolean> {
    try {
      const data = {
        order_id: order_id,
        overall_rating: overAllRating, // 1 to 5
        dishes_rating: [] as { dish_id: number; rating: number }[]
      }
      for (let i = 0; i < order.dishes.length; i++) {
        data.dishes_rating.push({
          dish_id: order.dishes[i].dish_id,
          rating: 1
        } as { dish_id: number; rating: number }) // Add type annotation here
      }
      const response = await fetch('/api/main/add_review', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      if (response.status !== 200) {
        throw new Error('Add review failed')
      }
      return true
    } catch (error) { 
      console.error(`POST /api/main/add_review`, error)
      throw error
    }
  }
}
