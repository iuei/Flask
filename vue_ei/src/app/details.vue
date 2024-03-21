<template>
  <el-row class="center-row">
    <!-- 用户信息列 -->
    <el-col :span="20">
      <el-descriptions class="margin-top details-height" title="个人详情" :column="3" :size="20" border>
        <template slot="extra">
          <el-button type="primary" size="small">操作</el-button>
        </template>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-user"></i>
            用户名
          </template>
          kooriookami
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-mobile-phone"></i>
            手机号
          </template>
          18100000000
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-location-outline"></i>
            居住地
          </template>
          苏州市
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-tickets"></i>
            备注
          </template>
          <el-tag size="small">学校</el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building"></i>
            联系地址
          </template>
          江苏省苏州市吴中区吴中大道 1188 号
        </el-descriptions-item>
      </el-descriptions>
    </el-col>

    <!-- 表格列 -->

  </el-row>
</template>

<script>
export default {
  name: "Details",
  data() {
    return {
      // 用户头像图片路径
      imgUrl: require('../static/jpg/2.jpg'),
      // 当前日期
      value: new Date(),
      // 登录时间戳
      loginTimestamp: null,
      name:'',
    }
  },
  mounted() {
    // 从本地存储中获取登录时间戳
    const loginTimestamp = localStorage.getItem('loginTimestamp');
    if (loginTimestamp) {
      // 将时间戳直接转换为可读的日期时间格式
      this.loginTimestamp = new Date(parseInt(loginTimestamp, 10)).toLocaleString();
    }
  }
}
</script>

<style scoped>
.center-row {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh; /* 将高度设置为视窗高度，实现垂直居中 */
}

.details-height {
  height: 600px; /* 设置描述列表的高度 */
}
</style>
