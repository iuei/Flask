<template>
  <el-container>
    <div class="imgUrl">
      <router-link to="/monitor" class="custom-link">首页</router-link>
      <div class="login-info">
        <!-- 居中显示登录时间 -->
        <p v-if="loginTimestamp" class="login-time center-text">上次登录: {{ loginTimestamp }}</p>
      </div>
      <div class="btn">
        <el-button @click="loginOut" type="warning" plain>退出</el-button>
      </div>
    </div>
  </el-container>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      // 登录时间戳
      loginTimestamp: null,
    };
  },
  methods: {
    // 退出登录
    loginOut() {
      // this.$confirm('是否退出','提示',{
      //   confirmButtonText:'确定',
      //   cancelButtonText:'取消',
      //   type:'warning'
      // })
        localStorage.removeItem('token');
        this.$router.push('/login')
    },
    home(){
      this.$router.push('/home')
    }
  },
  mounted() {
    // 从本地存储中获取登录时间戳
    const loginTimestamp = localStorage.getItem('loginTimestamp');
    if (loginTimestamp) {
      // 将时间戳转换为可读的日期时间格式
      this.loginTimestamp = new Date(parseInt(loginTimestamp, 10)).toLocaleString();
    }
  }
};
</script>

<style>
.el-header img {
  vertical-align: middle;
}

.imgUrl {
  color: #000000;
  /* 渲染背景图片 */
  /* background: url('../../../src/assets/20211206193128.jpg'); */
  /* 渲染背景色 */
  background: #90c2f5;
  background-size: 100% 100%;
  width: 100%;
  height: 60px;
}

.titleText {
  float: left;
  margin-left:20px
}
.custom-link {
  margin-left: 30px;
}
.btn {
  float: right;
  margin-right:20px
}
.imgUrl {
  display: flex; /* 使用 flexbox */
  justify-content: space-between; /* 在项目之间对齐 */
  align-items: center; /* 垂直居中对齐项目 */
  color: #000000;
  background: #90c2f5;
  background-size: 100% 100%;
  width: 100%;
  height: 60px;
}
.titleText {
  float: left;
  margin-left: 20px;
}

.custom-link {
  margin-left: 30px;
}

.btn {
  float: right;
  margin-right: 20px;
}
.center-text {
  text-align: center; /* 文本居中对齐 */
}
</style>
