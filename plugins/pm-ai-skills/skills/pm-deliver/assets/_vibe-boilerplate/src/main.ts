import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

import router from './router'
import App from './App.vue'
import './theme/style.css'
import { initTheme } from './theme/applyTheme'

initTheme()

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ArcoVue)
app.mount('#app')
