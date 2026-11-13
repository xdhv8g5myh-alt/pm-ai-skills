<script setup lang="ts">
import { computed } from 'vue'
import { useLayoutStore } from '@/stores/layout'

const layout = useLayoutStore()

interface KpiItem { label: string; value: string; change: string; up: boolean }
const kpis: KpiItem[] = [
  { label: '总销售额',   value: '¥ 1,284,530', change: '+12.5%', up: true  },
  { label: '新增订单',   value: '2,486',       change: '+8.2%',  up: true  },
  { label: '活跃用户',   value: '18,342',      change: '-2.1%',  up: false },
  { label: '转化率',     value: '3.84%',       change: '+0.6%',  up: true  },
]

interface OrderRow { id: string; customer: string; amount: number; status: string; date: string }
const orders: OrderRow[] = [
  { id: 'SO-20240115-001', customer: '北京科技有限公司', amount: 125800, status: '已完成',   date: '2024-01-15' },
  { id: 'SO-20240115-002', customer: '上海贸易集团',     amount: 89600,  status: '处理中',   date: '2024-01-15' },
  { id: 'SO-20240114-003', customer: '广州电子科技',     amount: 234500, status: '待审核',   date: '2024-01-14' },
  { id: 'SO-20240114-004', customer: '深圳信息股份',     amount: 56700,  status: '已完成',   date: '2024-01-14' },
  { id: 'SO-20240113-005', customer: '杭州网络技术',     amount: 178900, status: '已取消',   date: '2024-01-13' },
]

const tableClass = computed(() => `arco-table density-${layout.tableDensity}`)
</script>

<template>
  <!-- KPI 卡片 -->
  <a-row :gutter="16" style="margin-bottom:16px">
    <a-col :xs="24" :sm="12" :lg="6" v-for="k in kpis" :key="k.label">
      <div class="kpi-card" style="margin-bottom:16px">
        <div class="kpi-label">{{ k.label }}</div>
        <div class="kpi-value">{{ k.value }}</div>
        <div :class="['kpi-change', k.up ? 'up' : 'down']" style="margin-top:8px;font-size:13px">
          <span :class="['fas', k.up ? 'fa-arrow-up' : 'fa-arrow-down']" style="margin-right:4px" />
          {{ k.change }} 较上周
        </div>
      </div>
    </a-col>
  </a-row>

  <!-- 图表区域 -->
  <a-row :gutter="16" style="margin-bottom:16px">
    <a-col :xs="24" :lg="14">
      <a-card>
        <template #title>销售趋势</template>
        <div style="height:260px;border:2px dashed var(--proto-border);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#c9cdd4">
          <span class="fas fa-chart-line" style="font-size:32px;margin-right:12px" />
          图表占位（pm-deliver 可替换为 ECharts / Shadcn Chart）
        </div>
      </a-card>
    </a-col>
    <a-col :xs="24" :lg="10">
      <a-card>
        <template #title>渠道占比</template>
        <div style="height:260px;border:2px dashed var(--proto-border);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#c9cdd4">
          <span class="fas fa-chart-pie" style="font-size:32px;margin-right:12px" />
          图表占位
        </div>
      </a-card>
    </a-col>
  </a-row>

  <!-- 表格：最新订单 -->
  <a-card>
    <template #title>
      <span style="display:inline-flex;align-items:center;gap:8px">
        <span class="pro-block-title" style="margin:0">最新订单</span>
      </span>
    </template>
    <a-table :data="orders" :bordered="false" class="density-medium">
      <template #columns>
        <a-table-column title="订单号"   data-index="id" :width="180" />
        <a-table-column title="客户"     data-index="customer" />
        <a-table-column title="金额"     data-index="amount" :width="140" align="right">
          <template #cell="{ record }">¥ {{ record.amount.toLocaleString() }}</template>
        </a-table-column>
        <a-table-column title="状态"     data-index="status" :width="100">
          <template #cell="{ record }">
            <a-tag v-if="record.status === '已完成'" color="green">{{ record.status }}</a-tag>
            <a-tag v-else-if="record.status === '处理中'" color="blue">{{ record.status }}</a-tag>
            <a-tag v-else-if="record.status === '待审核'" color="orange">{{ record.status }}</a-tag>
            <a-tag v-else color="red">{{ record.status }}</a-tag>
          </template>
        </a-table-column>
        <a-table-column title="日期"     data-index="date" :width="120" />
      </template>
    </a-table>
  </a-card>
</template>
