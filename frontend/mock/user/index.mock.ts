

// const timeout = 1000

// const List: {
//   username: string
//   password: string
//   role: string
//   roleId: string
//   permissions: string | string[]
// }[] = [
//   {
//     username: 'admin',
//     password: 'admin',
//     role: 'admin',
//     roleId: '1',
//     permissions: ['*.*.*']
//   },
//   {
//     username: 'test',
//     password: 'test',
//     role: 'test',
//     roleId: '2',
//     permissions: ['example:dialog:create', 'example:dialog:delete']
//   }
// ]

// export default [
//   // 列表接口
//   {
//     url: '/mock/user/list',
//     method: 'get',
//     response: ({ query }) => {
//       const { username, pageIndex, pageSize } = query

//       const mockList = List.filter((item) => {
//         if (username && item.username.indexOf(username) < 0) return false
//         return true
//       })
//       const pageList = mockList.filter(
//         (_, index) => index < pageSize * pageIndex && index >= pageSize * (pageIndex - 1)
//       )

//       return {
//         code: SUCCESS_CODE,
//         data: {
//           total: mockList.length,
//           list: pageList
//         }
//       }
//     }
//   }
// ]
