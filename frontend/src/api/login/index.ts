import request from '@/axios'
import type { UserType } from './types'
import { SUCCESS_CODE } from '@/constants'

interface RoleParams {
  roleName: string
}

const List: {
  username: string
  password: string
  role: string
  roleId: string
  permissions: string | string[]
}[] = [
  {
    username: 'admin',
    password: 'admin',
    role: 'admin',
    roleId: '1',
    permissions: ['*.*.*']
  },
  {
    username: 'test',
    password: 'test',
    role: 'test',
    roleId: '2',
    permissions: ['example:dialog:create', 'example:dialog:delete']
  }
]

export const loginApi = (data: UserType): any => {}

export const loginOutApi = () => {}

export const getAdminRoleApi = (params: RoleParams) => {}

export const getTestRoleApi = (params: RoleParams) => {}
