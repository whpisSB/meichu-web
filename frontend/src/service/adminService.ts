import type { restaurant, chart, order } from '../types/restaurant'

export default class adminService {
  static async addNewRestaurant(token: string, restaurant: any): Promise<boolean> {
    try {
      const response = await fetch('/api/admin/add_restaurant', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(restaurant)
      })
      if (response.status != 200) {
        throw new Error('Permission Denied')
      }
      const data = await response.json()
      const restaurant_id = data.restaurant_id
      const formData = new FormData()
      formData.append('image', restaurant.picture)
      formData.append('restaurant_id', restaurant_id)
      const response2 = await fetch('/api/admin/upload/cover', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + token
        },
        body: formData
      })
      console.log(await response2.json())
      if (response2.status != 200) {
        throw new Error('Permission Denied')
      }
      return true
    } catch (error) {
      throw error
      return false
    }
  }
  static async addNewMeal(token: string, meal: any): Promise<boolean> {
      try {
        const formData = new FormData()
        formData.append('image', meal.picture)
        const response = await fetch('/api/admin/upload/dish', {
          method: 'POST',
          headers: {
            Authorization: 'Bearer ' + token
          },
          body: formData
        })
        const filename = await response.json()
        console.log(filename.filename)
        const response2 = await fetch('/api/admin/add_dish', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            restaurant_id: meal.restaurant_id,
            name: meal.name,
            price: meal.price,
            description: meal.description,
            picture_filename: filename.filename,
            combo: meal.combo
          })
        })  
        console.log(await response2.json())
        if (response2.status != 200) {
          throw new Error('Permission Denied')
        }
      }
      catch (error) {
        throw error
        return false
      }

    return true
  }
  static async downloadMonthlyReport(token: string, year: number, month: number): Promise<any> {
    try {
      const response = await fetch('/api/admin/monthly_report', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ year: year, month: month })
      })
      if (response.status != 200) {
        throw new Error('Download Failed')
      }
      return await response.blob()
    } catch (error) {
      console.log('/api/admin/monthly_report', error)
      return null
    }
  }
  static async updateMealPrice(token: string, mealPrice: any): Promise<boolean> {
    try {
      const response = await fetch('/api/admin/update_price', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(mealPrice)
      })
      if (response.status != 200) {
        throw new Error('Permission Denied')
      }
      return true
    }
    catch (error) {
      throw error
    }
  }
  static async updateMenu(token: string, menu: any): Promise<boolean> {
    try { 
      console.log(menu)
      const response = await fetch('/api/admin/update_menu', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          available_dish_id: menu
        
        })
      })
      if (response.status != 200) {
        throw new Error('Permission Denied')
      }
      return true
    }
    catch (error) {
      throw error
    }
  }
}
