import { describe, test, expect, vi , beforeEach} from 'vitest'
import userService from '../service/userService'
import createFetchMock from 'vitest-fetch-mock';

const token = 'token' 
const fetchMocker = createFetchMock(vi);

describe('Testing for User Service', () => {
    beforeEach(() => {
        fetchMocker.enableMocks()
    });

    test('User Login with correct username and password', async () => {
        const username = 'test'
        const password = 'test'
        fetchMocker.mockResponseOnce(JSON.stringify({ outh_token: "", user_identity: "restaurant", restaurant_id: 1 }), { status: 200 })

        const response = await userService.userLogin(username, password);

        expect(response).toEqual({ outh_token: "", user_identity: "restaurant", restaurant_id: 1 })
    })

    test('User Login with incorrect username and password', async () => {
        const username = 'test'
        const password = 'test'
        fetchMocker.mockResponseOnce(JSON.stringify({ outh_token: "", user_identity: "invalid_user", restaurant_id: "" }), { status: 200 })

        const response = await userService.userLogin(username, password);

        expect(response.user_identity).toEqual("invalid_user")
    })
})