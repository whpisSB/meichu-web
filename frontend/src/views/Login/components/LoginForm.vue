<script setup lang="tsx">
import { reactive, ref, watch, onMounted, unref } from 'vue'
import { Form, FormSchema } from '@/components/Form'
import { useI18n } from '@/hooks/web/useI18n'
import { ElCheckbox } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import loginService from '@/api/login/loginService.ts'
import { useAppStore } from '@/store/modules/app'
import { usePermissionStore } from '@/store/modules/permission'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalizedLoaded, RouteRecordRaw } from 'vue-router'
import { UserType } from '@/api/login/types'
import { useValidator } from '@/hooks/web/useValidator'
import { useUserStore } from '@/store/modules/user'
import { BaseButton } from '@/components/Button'
import { ElNotification } from 'element-plus'
import { format } from 'path'
const { required } = useValidator()

const emit = defineEmits(['to-register'])

const appStore = useAppStore()

const userStore = useUserStore()

const permissionStore = usePermissionStore()

const { currentRoute, addRoute, push } = useRouter()

const { t } = useI18n()

const rules = {
  username: [required()],
  password: [required()]
}

const schema = reactive<FormSchema[]>([
  {
    field: 'title',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return <h2 class="text-2xl font-bold text-center w-[100%]">{t('login.login')}</h2>
        }
      }
    }
  },
  {
    field: 'username',
    label: t('login.username'),
    // value: 'admin',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      placeholder: 'admin or test'
    }
  },
  {
    field: 'password',
    label: t('login.password'),
    // value: 'admin',
    component: 'InputPassword',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '100%'
      },
      placeholder: 'admin or test'
    }
  },
  {
    field: 'tool',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="flex justify-between items-center w-[100%]">
                <ElCheckbox v-model={remember.value} label={t('login.remember')} size="small" />
              </div>
            </>
          )
        }
      }
    }
  },
  {
    field: 'login',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="w-[100%]">
                <BaseButton
                  loading={loading.value}
                  type="primary"
                  class="w-[100%]"
                  onClick={signIn}
                >
                  {t('login.login')}
                </BaseButton>
              </div>
              <div class="w-[100%] mt-15px">
                <button class="w-[100%]" onClick={testPing}>
                  {t('login.register')}
                </button>
              </div>
            </>
          )
        }
      }
    }
  }
])
const remember = ref(userStore.getRememberMe)

const initLoginInfo = () => {
  const loginInfomation = userStore.getLoginInfo
  if (loginInfomation) {
    const { username, password } = loginInfomation
    setValues({ username, password })
  }
}
onMounted(() => {
  initLoginInfo()
})

const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose, setValues } = formMethods

const loading = ref(false)

const redirect = ref<string>('')

watch(
  () => currentRoute.value,
  (route: RouteLocationNormalizedLoaded) => {
    redirect.value = route?.query?.redirect as string
  },
  {
    immediate: true
  }
)

// 登录
const testPing = async (): Promise<void> => {
  console.log('testPing')
  const userInfo = {
    user_account: 'ycy.yo@gmail.com',
    user_password: 'password'
  }
  const testFetch = await loginService.loginApi(userInfo)
  console.log('testFetch', testFetch)
}
const signIn = async () => {
  const formRef = await getElFormExpose()
  await formRef?.validate(async (isValid) => {
    if (isValid) {
      loading.value = true
      const formData = await getFormData<UserType>()
      console.log(formData)
      // const res = loginApi(formData)
      const result = await loginService.loginApi({
        user_account: formData.username,
        user_password: formData.password
      })
      if (result === true) {
        const res = {
          username: formData.username,
          password: formData.password,
          role: 'admin',
          roleId: '1',
          permissions: ['*.*.*']
        }
        if (unref(remember)) {
          userStore.setLoginInfo({
            username: formData.username,
            password: formData.password
          })
        } else {
          userStore.setLoginInfo(undefined)
        }
        userStore.setRememberMe(unref(remember))
        userStore.setUserInfo(res)
        // 是否使用动态路由
        if (appStore.getDynamicRouter) {
          getRole()
        } else {
          await permissionStore.generateRoutes('static').catch(() => {})
          permissionStore.getAddRouters.forEach((route) => {
            addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
          })
          permissionStore.setIsAddRouters(true)
          console.log(redirect.value)
          push({ path: redirect.value || permissionStore.addRouters[0].path })
        }
      } else {
        ElNotification({
          title: '錯誤帳號密碼',
          type: 'error',
          duration: 1000,
          dangerouslyUseHTMLString: true,
          message: '你的帳號密碼錯誤，請你重新登入'
        })
      }
    }
  })
}

// 获取角色信息
const adminList = [
  {
    path: '/dashboard',
    component: '#',
    redirect: '/dashboard/analysis',
    name: 'Dashboard',
    meta: {
      title: 'router.dashboard',
      icon: 'vi-ant-design:dashboard-filled',
      alwaysShow: true
    },
    children: [
      {
        path: 'analysis',
        component: 'views/Dashboard/Analysis',
        name: 'Analysis',
        meta: {
          title: 'router.analysis',
          noCache: true,
          affix: true
        }
      },
      {
        path: 'workplace',
        component: 'views/Dashboard/Workplace',
        name: 'Workplace',
        meta: {
          title: 'router.workplace',
          noCache: true,
          affix: true
        }
      }
    ]
  },
  {
    path: '/product',
    component: '#',
    name: '購物車',
    meta: {},
    children: [
      {
        path: 'index',
        component: 'views/Guide/Guide',
        name: 'GuideDemo',
        meta: {
          title: '購物車',
          icon: 'vi-cib:telegram-plane'
        }
      }
    ]
  }
]

const getRole = async () => {
  const formData = await getFormData<UserType>()
  const res = appStore.getDynamicRouter && appStore.getServerDynamicRouter ? adminList : adminList
  const routers = res || []
  console.log('fuck you', routers)
  userStore.setRoleRouters(routers)
  appStore.getDynamicRouter && appStore.getServerDynamicRouter
    ? await permissionStore.generateRoutes('server', routers).catch(() => {})
    : await permissionStore.generateRoutes('frontEnd', routers).catch(() => {})

  permissionStore.getAddRouters.forEach((route) => {
    addRoute(route as RouteRecordRaw) // 动态添加可访问路由表
  })
  permissionStore.setIsAddRouters(true)
  push({ path: redirect.value || permissionStore.addRouters[0].path })
}

// 去注册页面
const toRegister = () => {
  emit('to-register')
}
</script>

<template>
  <Form
    :schema="schema"
    :rules="rules"
    label-position="top"
    hide-required-asterisk
    size="large"
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
    @register="formRegister"
  />
</template>
