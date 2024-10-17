interface meal {
  dish_id: number
  name: string
  description: string
  combo: boolean
  price: number
  rating: number
  order_times: number
  picture: string
}

interface dish {
  dish_id: number
  dish_name: string
  number: number
  price: number
  rating: number
}

interface restaurant {
  id: number
  restaurant: string
  phone: string
  picture: string
  description: string
  rating: number
  open_time: string
  close_time: string
  meals: meal[]
  url?: string
}

interface order {
  order_id: number
  order_time: string
  restaurant_id: number
  total_price: number
  finished: boolean
  reviewed: boolean
  overall_rating: number
  restaurant_name: string
  dishes: dish[]
}

interface orderReview {
  order_id: number
  overall_rating: number
  dishes_rating: {
    dish_id: number
    rating: number
  }[]
}

export { type restaurant, type meal, type dish, type order, type orderReview }
