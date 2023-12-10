import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';


// Add the solid icons to the library
library.add(fas);

const app = createApp(App)

app.use(router)
app.mount('#app')
