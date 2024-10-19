// import Mock from 'mockjs'
// import { SUCCESS_CODE } from '@/constants'
// import { toAnyString } from '@/utils'

// const timeout = 1000




// const List: any[] = []

// const roleNames = ['超级管理员', '管理员', '普通用户', '游客']
// const menus = [
//   [
//     {
//       path: '/dashboard',
//       component: '#',
//       redirect: '/dashboard/analysis',
//       name: 'Dashboard',
//       status: Mock.Random.integer(0, 1),
//       id: 1,
//       meta: {
//         title: '首页',
//         icon: 'vi-ant-design:dashboard-filled',
//         alwaysShow: true
//       },
//       children: [
//         {
//           path: 'analysis',
//           component: 'views/Dashboard/Analysis',
//           name: 'Analysis',
//           status: Mock.Random.integer(0, 1),
//           id: 2,
//           meta: {
//             title: '分析页',
//             noCache: true
//           }
//         },
//         {
//           path: 'workplace',
//           component: 'views/Dashboard/Workplace',
//           name: 'Workplace',
//           status: Mock.Random.integer(0, 1),
//           id: 3,
//           meta: {
//             title: '工作台',
//             noCache: true
//           }
//         }
//       ]
//     },
//   ],
//   [
//     {
//       path: '/dashboard',
//       component: '#',
//       redirect: '/dashboard/analysis',
//       name: 'Dashboard',
//       status: Mock.Random.integer(0, 1),
//       id: 1,
//       meta: {
//         title: '首页',
//         icon: 'vi-ant-design:dashboard-filled',
//         alwaysShow: true
//       },
//       children: [
//         {
//           path: 'analysis',
//           component: 'views/Dashboard/Analysis',
//           name: 'Analysis',
//           status: Mock.Random.integer(0, 1),
//           id: 2,
//           meta: {
//             title: '分析页',
//             noCache: true
//           }
//         },
//         {
//           path: 'workplace',
//           component: 'views/Dashboard/Workplace',
//           name: 'Workplace',
//           status: Mock.Random.integer(0, 1),
//           id: 3,
//           meta: {
//             title: '工作台',
//             noCache: true
//           }
//         }
//       ]
//     }
//   ],
//   []
// ]

// for (let i = 0; i < 4; i++) {
//   List.push(
//     Mock.mock({
//       id: toAnyString(),
//       // timestamp: +Mock.Random.date('T'),
//       roleName: roleNames[i],
//       role: '@first',
//       status: Mock.Random.integer(0, 1),
//       createTime: '@datetime',
//       remark: '@cword(10, 15)',
//       menu: menus[i]
//     })
//   )
// }

// export default [
//   // 列表接口
// ]
