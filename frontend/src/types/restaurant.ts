interface meal {
  dish_id: number
  name: string
  description: string
  combo: boolean
  price: number
  rating: number
  order_times: number
  picture: string
  available: number
}

interface chart {
  customer_id: number
  total_price: number
  dishes: {
    dish_id: number
    number: number
  }[]
}

interface restaurant {
  restaurant: string
  meals: meal[]
}

interface order {
  order_id: number
  customer_id: number
  customer_name: string
  order_time: string
  finish: boolean
  price: number
  dishes: {
    dish_id: number
    dish_name: string
    number: number
    price: number
  }[]
}

export { type restaurant, type meal, type chart, type order }
