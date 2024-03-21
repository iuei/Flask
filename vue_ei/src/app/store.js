// src/app/store.js

// 导入 Vuex 库中的 createStore 函数
import { createStore } from 'vuex';

// 创建 Vuex Store，用于管理应用程序的状态
const store = createStore({
    // 应用程序的状态
    state() {
        return {
            // 当前登录的用户信息，默认为 null
            user: null,
            // 用户的身份验证令牌，默认从本地存储中获取，如果不存在则为 null
            token: localStorage.getItem('token') || null,
        };
    },
    // Mutations 用于修改状态
    mutations: {
        // 设置当前用户信息
        setUser(state, user) {
            state.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        },
        // 设置身份验证令牌，并将其存储在本地存储中
        setToken(state, token) {
            state.token = token;
            localStorage.setItem('token', token);
        },
        // 注销用户，将用户信息和令牌设置为 null，并从本地存储中移除令牌
        logout(state) {
            state.user = null;
            state.token = null;
            localStorage.removeItem('token');
        },
    },
    // Actions 用于处理异步操作
    actions: {
        // 在这里可以添加应用程序和注销的异步操作
    },
    // Getters 用于定义计算属性
    getters: {
        // 在这里可以定义 getters，用于派生状态的衍生值
    },
});

// 导出创建的 Vuex Store，以便在应用程序的入口文件中引入和使用
export default store;
