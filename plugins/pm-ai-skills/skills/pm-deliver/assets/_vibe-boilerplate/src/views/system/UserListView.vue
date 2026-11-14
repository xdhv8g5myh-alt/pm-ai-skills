<script setup lang="ts">
import { ref } from 'vue'

interface UserRow { id: number; name: string; dept: string; role: string; email: string; status: string; createdAt: string }
const allUsers: UserRow[] = [
  { id: 1,  name: '张伟',   dept: '产品部',   role: '产品经理', email: 'zhangwei@example.com',   status: '启用', createdAt: '2024-01-10' },
  { id: 2,  name: '李娜',   dept: '技术部',   role: '前端工程师', email: 'lina@example.com',     status: '启用', createdAt: '2024-01-08' },
  { id: 3,  name: '王强',   dept: '技术部',   role: '后端工程师', email: 'wangqiang@example.com', status: '启用', createdAt: '2024-01-05' },
  { id: 4,  name: '刘洋',   dept: '设计部',   role: 'UI设计师',  email: 'liuyang@example.com',   status: '启用', createdAt: '2024-01-03' },
  { id: 5,  name: '陈静',   dept: '产品部',   role: '产品运营',  email: 'chenjing@example.com',  status: '禁用', createdAt: '2023-12-28' },
  { id: 6,  name: '赵敏',   dept: '技术部',   role: '测试工程师', email: 'zhaomin@example.com',   status: '启用', createdAt: '2023-12-25' },
]

const filters = ref({ dept: '', role: '', keyword: '' })

const filtered = ref<UserRow[]>([...allUsers])

function onFilter() {
  filtered.value = allUsers.filter(u =>
    (!filters.value.dept  || u.dept  === filters.value.dept) &&
    (!filters.value.role  || u.role  === filters.value.role) &&
    (!filters.value.keyword || u.name.includes(filters.value.keyword) || u.email.includes(filters.value.keyword))
  )
}
function onReset() {
  filters.value = { dept: '', role: '', keyword: '' }
  filtered.value = [...allUsers]
}
</script>

<template>
  <!-- 左侧筛选面板 + 右侧表格 -->
  <a-row :gutter="16">
    <!-- 筛选面板 -->
    <a-col :xs="24" :lg="6">
      <a-card title="筛选条件">
        <a-form :model="filters" layout="vertical">
          <a-form-item label="关键词">
            <a-input v-model="filters.keyword" placeholder="姓名 / 邮箱" allow-clear />
          </a-form-item>
          <a-form-item label="部门">
            <a-select v-model="filters.dept" placeholder="全部" allow-clear>
              <a-option value="产品部">产品部</a-option>
              <a-option value="技术部">技术部</a-option>
              <a-option value="设计部">设计部</a-option>
            </a-select>
          </a-form-item>
          <a-form-item label="角色">
            <a-select v-model="filters.role" placeholder="全部" allow-clear>
              <a-option value="产品经理">产品经理</a-option>
              <a-option value="前端工程师">前端工程师</a-option>
              <a-option value="后端工程师">后端工程师</a-option>
              <a-option value="UI设计师">UI设计师</a-option>
            </a-select>
          </a-form-item>
          <div style="display:flex;gap:8px">
            <a-button type="primary" @click="onFilter" long>查询</a-button>
            <a-button @click="onReset" long>重置</a-button>
          </div>
        </a-form>
      </a-card>
    </a-col>

    <!-- 表格区 -->
    <a-col :xs="24" :lg="18">
      <a-card>
        <template #title>
          <span class="pro-block-title" style="margin:0">用户列表（{{ filtered.length }} 条）</span>
        </template>
        <template #extra>
          <a-space>
            <a-button type="primary">
              <span class="fas fa-plus" style="margin-right:4px" />新增用户
            </a-button>
            <a-button>导出</a-button>
          </a-space>
        </template>

        <a-table :data="filtered" :bordered="false" :pagination="{ pageSize: 10 }">
          <template #columns>
            <a-table-column title="ID"       data-index="id" :width="60" />
            <a-table-column title="姓名"     data-index="name" :width="100" />
            <a-table-column title="部门"     data-index="dept" :width="100" />
            <a-table-column title="角色"     data-index="role" :width="120" />
            <a-table-column title="邮箱"     data-index="email" />
            <a-table-column title="状态"     data-index="status" :width="80">
              <template #cell="{ record }">
                <a-tag :color="record.status === '启用' ? 'green' : 'red'">{{ record.status }}</a-tag>
              </template>
            </a-table-column>
            <a-table-column title="创建时间" data-index="createdAt" :width="120" />
            <a-table-column title="操作"     :width="140" fixed="right">
              <template #cell>
                <a-space>
                  <a-link>编辑</a-link>
                  <a-link>详情</a-link>
                </a-space>
              </template>
            </a-table-column>
          </template>
        </a-table>
      </a-card>
    </a-col>
  </a-row>
</template>
