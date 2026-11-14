<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route  = useRoute()

const form = reactive({ username: 'admin', password: '123456' })
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  await new Promise(r => setTimeout(r, 500))
  const ok = auth.login(form.username, form.password)
  loading.value = false

  if (ok) {
    Message.success('登录成功')
    const redirect = (route.query.redirect as string) || '/dashboard'
    router.push(redirect)
  } else {
    Message.error('用户名或密码错误（试试 admin / 123456）')
  }
}
</script>

<template>
  <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgb(var(--primary-6)),rgb(var(--primary-4,175 164 243)));">
    <a-card :bordered="false" style="width:400px;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.2)">
      <h2 style="margin:0 0 4px;font-size:22px">Vibe Admin</h2>
      <p style="margin:0 0 24px;color:#86909c;font-size:13px">pm-deliver 中后台母板 · 请登录</p>

      <a-form :model="form" layout="vertical" @submit="handleLogin">
        <a-form-item field="username" label="用户名">
          <a-input v-model="form.username" placeholder="admin" allow-clear />
        </a-form-item>
        <a-form-item field="password" label="密码">
          <a-input-password v-model="form.password" placeholder="123456" />
        </a-form-item>
        <a-button type="primary" long :loading="loading" html-type="submit" style="margin-top:8px">
          登 录
        </a-button>
        <p style="margin-top:12px;color:#86909c;font-size:12px;text-align:center">
          演示账号：admin / 123456
        </p>
      </a-form>
    </a-card>
  </div>
</template>
