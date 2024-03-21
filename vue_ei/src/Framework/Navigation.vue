<template>
  <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" :style="{ width: '200px', height: '100%' }">
    <div class="centered-container">
      <el-avatar :size="100" :src="imgUrl"></el-avatar>
      <p>{{ displayUserRole }}：{{user_data.name}}</p>
    </div>
    <el-submenu v-for="submenu in menuData" :key="submenu.index" :index="submenu.index" :style="{ width: '200px' }">
      <template slot="title">
        <i :class="submenu.icon"></i>
        <span>{{ submenu.title }}</span>
      </template>
      <el-menu-item-group v-for="group in submenu.groups" :key="group.title" :title="group.title">
        <router-link v-for="item in group.items" :key="item.index" :to="{ name: item.route }">
          <el-menu-item :index="item.index" @click="handleMenuItemClick(item)">
            {{ item.title }}
          </el-menu-item>
        </router-link>
      </el-menu-item-group>
    </el-submenu>
  </el-menu>
</template>

<script>
import router from "../router";
import store from "../app/store";

export default {
  data() {
    return {
      user_data: {
        name: '',
        user_type: ''
      },
      baseUrl: 'http://localhost:5000',
      imgUrl: require('../static/jpg/头像.jpg'),
      activeMenu: '2',
      menuData: [
        {
          index: '1', icon: 'el-icon-menu', title: '商品',
          groups: [
            { items: [{ index: '1-1', title: '商品管理', route: 'commodity_list' }] },
            { items: [{ index: '1-2', title: '商品列表', route: 'sell' }] },
          ],
        },
        {
          index: '2', icon: 'el-icon-menu', title: '用户管理',
          groups: [
            { items: [{ index: '2-1', title: '用户列表', route: 'user_list' }] },
            { items: [{ index: '2-2', title: '员工列表', route: 'employees_list' }] },
          ],
        },
        {
          index: '3', icon: 'el-icon-document', title: '导航三',
        },
        {
          index: '4', icon: 'el-icon-setting', title: '设置',
          groups: [
            { items: [{ index: '4-1', title: '详情', route: 'Details' }] },
          ],
        },
      ],
    };
  },
  computed: {
    displayUserRole() {
      switch (this.user_data.user_type) {
        case '1':
          return '普通用户';
        case '2':
          return '会员';
        case '3':
          return '管理员';
        default:
          return '';
      }
    },
  },
  methods: {
    handleMenuItemClick(item) {
      if (item.route) {
        router.push({ name: item.route });
      }
    },
    getUserInfo() {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        const user = JSON.parse(storedUser);
        this.user_data.name = user.username;
        this.user_data.user_type = user.user_type;
      } else {
        console.log('用户信息获取失败');
      }
    },
  },
  mounted() {
    this.getUserInfo();
  },
};
</script>

<style scoped>
.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.el-tabs__nav-wrap::after{
  position:static !important;
}
.el-tabs__active-bar{
  background-color:transparent !important;
}
</style>
