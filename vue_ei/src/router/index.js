import Vue from 'vue';
import Router from 'vue-router';
import login from "../app/login.vue";
import commodity_list from "../app/commodity_list.vue";
import home from "../home/Home.vue";
import user_list from "../app/user_list.vue";
import monitor from "../app/monitor.vue";
import Details from "../app/details.vue";
import employees_list from "../app/employees_list.vue";
import sell from "../app/shopping_cart.vue";

Vue.use(Router);

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: login,
    },

    {
        path: '/home',
        name: 'home',
        component: home,
        children: [
            {
                path: '/monitor',
                name: 'Monitor',
                component: monitor,
                meta: { requiresAuth: true },
            },
            {
                path: '/commodity_list',
                name: 'commodity_list',
                component: commodity_list,
                meta: { requiresAuth: true },
            },
            {
                path: '/sell',
                name: 'sell',
                component: sell,
                meta: { requiresAuth: true },
            },
            {
                path: '/employees_list',
                name: 'employees_list',
                component: employees_list,
                meta: { requiresAuth: true },
            },
            {
                path: '/user_list',
                name: 'user_list',
                component: user_list,
                meta: { requiresAuth: true },
            },
            {
                path: '/details',
                name: 'Details',
                component: Details,
                meta: { requiresAuth: true },
            },
        ],
    },
];


const router = new Router({
    mode: 'history',
    routes,
});

// Vue Router全局导航守卫
router.beforeEach((to, from, next) => {
    // 检查路由是否需要身份验证
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    // 从localStorage中获取令牌
    const token = localStorage.getItem('token');

    // 如果路由需要身份验证且没有令牌
    if (requiresAuth && !token) {
        // 重定向到登录页面，并将原始路径保存为查询参数
        Vue.prototype.$message.warning('请先登录再访问');
        next({
            path: '/login',
            query: { redirect: to.fullPath }
        });
    } else if (token && to.path === '/login') {
        // 如果有令牌且用户尝试访问登录页面，则自动重定向到'/monitor'
        next('/monitor');
    } else {
        // 允许导航继续
        next();
    }
});


export default router;
