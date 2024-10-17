import { describe, test, expect, vi , beforeEach} from 'vitest'
import restaurantService from '../service/restaurantService'
import createFetchMock from 'vitest-fetch-mock';

const fetchMocker = createFetchMock(vi);
const token = 'token' 

describe('Testing for Restaurant Service', () => {
    beforeEach(() => {
        fetchMocker.enableMocks()
    });

    test('Get Restaueant Menu with authorized token', async () => {
        const restaurant = 'Fake Restaurant'
        const meals = [{ id: 1, name: 'Meal 1' }, { id: 2, name: 'Meal 2' }, { id: 3, name: 'Meal 3' }, { id: 4, name: 'Meal 4' }]
        
        fetchMocker.mockResponseOnce(JSON.stringify({  meals }), { status: 200 })
        const response = await restaurantService.getRestaurant(token)

        expect(response).toEqual({ restaurant, meals })
    })

    test('Get Restaurant Menu with unauthorized token', async () => {
        
        fetchMocker.mockResponseOnce(JSON.stringify({  error: 'Permission Denied' }), { status: 403 })

        await expect(restaurantService.getRestaurant(token)).rejects.toThrowError(new Error('Permission Denied'))
    })

    test('Add Order with authorized token', async () => {
        const order_id = 1
        fetchMocker.mockResponseOnce(JSON.stringify({ order_id: order_id }), { status: 200 })
        
        const response = await restaurantService.addOrder(token, { customer_id: 1, total_price: 100, dishes: [{ dish_id: 1, number: 2 }, { dish_id: 2, number: 3 }] })

        expect(response).toEqual(order_id)
    })

    test('Add Order with unauthorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(restaurantService.addOrder(token, { customer_id: 1, total_price: 100, dishes: [{ dish_id: 1, number: 2 }, { dish_id: 2, number: 3 }]})).rejects.toThrowError(new Error('Permission Denied'))
    })

    test('Get History Order with authorized token', async () => {
        const orders = {orders: [{ id: 1, total_price: 100, dishes: [{ dish_id: 1, number: 2 }, { dish_id: 2, number: 3 }] }, { id: 2, total_price: 200, dishes: [{ dish_id: 3, number: 2 }, { dish_id: 4, number: 3 }] }]}
        fetchMocker.mockResponseOnce(JSON.stringify(orders), { status: 200 }) 

        const response = await restaurantService.getHistoryOrder(token)
        expect(response).toEqual(orders.orders)

    })

    test('Get History Order with unauthorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(restaurantService.getHistoryOrder(token)).rejects.toThrowError(new Error('Permission Denied'))
    })

    test('Finish Order with authorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ status: 'success' }), { status: 200 })
        const response = await restaurantService.finishOrder(token, 1)
        expect(response).toEqual(true)
    })

    test('Finish Order with unauthorized token', async () => {
        fetchMocker.mockResponseOnce(JSON.stringify({ error: 'Permission Denied' }), { status: 403 })
        await expect(restaurantService.finishOrder(token, 1)).rejects.toThrowError(new Error('Permission Denied'))
    })

})