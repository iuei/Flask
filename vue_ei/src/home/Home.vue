<template>
  <el-container class="home_container">
    <!-- 左侧导航栏 -->
    <el-aside style="width: 200px">
      <!-- 局部方法复用 -->
      <Navigation />
    </el-aside>

    <!-- 右侧内容区域 -->
    <el-container>
      <el-header style="height: 60px">
        <!-- 局部方法复用 -->
        <Header />
      </el-header>

      <el-container>
        <!-- 主体内容 -->
        <el-main>
          <!-- 路由统一跳转 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
// 引入Header、Navigation组件
import Header from "../Framework/Header.vue";
import Navigation from "../Framework/Navigation.vue";

export default {
  // 给组件命名为Home
  name: "Home",
  components: {
    // 复用Header组件
    Header,
    // 复用Navigation组件
    Navigation,
  },
  data() {
    return {};
  },
};
</script>

<style scoped="scoped">
.home_container {
  width: 100%;
  height: 100%;
  display: flex;
}

.el-aside {
  background: #333;
  overflow: hidden; /* Hide the scrollbar */
}

.Retract {
  color: rgba(255, 255, 255, 0.952);
}

.el-main {
  background: rgb(255, 255, 255);
}

.el-header {
  padding: 0px;
}
</style>

