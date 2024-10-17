import { describe, test, expect, vi , beforeEach} from 'vitest'
import workerService from '../service/workerService'
import createFetchMock from 'vitest-fetch-mock';

const token = 'token' 
const fetchMocker = createFetchMock(vi);

describe('Testing for Worker Service', () => {
    beforeEach(() => {
        fetchMocker.enableMocks()
    });
    const token = 'token'
    test('Get Restaurant list with authorized token', async () => {
        const restaurant_list = { restaurants: [{ id: 1, name: 'Restaurant 1' }, { id: 2, name: 'Restaurant 2' }, { id: 3, name: 'Restaurant 3' }, { id: 4, name: 'Restaurant 4' }] }
        fetchMocker.mockResponseOnce(JSON.stringify(restaurant_list)), { status: 200 }
        const response = await workerService.getRestaurantList(token)

        expect(response).toEqual(restaurant_list.restaurants)
    })

    test('Get Restaurant Info with authorized token', async () => {
        const restaurant = 'Fake Restaurant'
        const meals = [{ id: 1, name: 'Meal 1' }, { id: 2, name: 'Meal 2' }, { id: 3, name: 'Meal 3' }, { id: 4, name: 'Meal 4' }]
        fetchMocker.mockResponseOnce(JSON.stringify({ restaurant, meals }), { status: 200 })
        const response = await workerService.getRestaurant(token, '1')

        expect(response).toEqual({ restaurant, meals })
    })

    test('Get Restaurant Info with unauthorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(workerService.getRestaurant(token, '1')).rejects.toThrowError(new Error('Permission Denied'))
    })

    test('Get History Order with authorized token', async () => {
        const orders = [{ id: 1, total_price: 100, dishes: [{ dish_id: 1, number: 2 }, { dish_id: 2, number: 3 }] }, { id: 2, total_price: 200, dishes: [{ dish_id: 3, number: 2 }, { dish_id: 4, number: 3 }] }]
        fetchMocker.mockResponseOnce(JSON.stringify({ orders }), { status: 200 })
        const response = await workerService.getHistoryOrder(token)

        expect(response).toEqual(orders)
    })

    test('Get History Order with unauthorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(workerService.getHistoryOrder(token)).rejects.toThrowError(new Error('Permission Denied'))
    })

    test('Review Order with authorized token', async () => {
        const order_id = 1
        const overAllRating = 5
        const dishes = [{ dish_id: 1, dish_name: 'chicken', number:1, price: 3, rating: 5 }]
        const order = { order_id: 1, order_time: '2024', restaurant_id: 1, total_price: 100, finished: true, reviewed: false, overall_rating: 3, restaurant_name: 'test', dishes: dishes }
        fetchMocker.mockResponseOnce(JSON.stringify({ status: 'success'}), { status: 200 })
        const response = await workerService.reviewOrder(token, order_id, overAllRating, order)

        expect(response).toEqual(true)
    })

    test('Review Order Failed', async () => {
        const order_id = 1
        const overAllRating = 5
        const dishes = [{ dish_id: 1, dish_name: 'chicken', number:1, price: 3, rating: 5 }]
        const order = { order_id: 1, order_time: '2024', restaurant_id: 1, total_price: 100, finished: true, reviewed: false, overall_rating: 3, restaurant_name: 'test', dishes: dishes }

        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(workerService.reviewOrder(token, order_id, overAllRating, order)).rejects.toThrowError(new Error('Add review failed'))
    })

})