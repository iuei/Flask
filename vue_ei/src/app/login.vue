<template>
  <div class="login-container" >
    <el-form :model="loginForm" label-width="80px" class="login-form">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">登录</el-button>
        <el-button type="primary" @click="openRegisterDialog">注册</el-button>
      </el-form-item>
    </el-form>

    <el-dialog :visible.sync="registerDialogVisible" title="注册" width="30%" :close-on-click-modal="false" center>
      <el-form ref="registerForm" :model="registerForm" label-width="80px" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="cell">
          <el-input v-model="registerForm.cell" placeholder="请输入手机号" :maxlength="11"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="register">注册</el-button>
          <el-button type="primary" @click="returnLogin">返回</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import store from './store';
import Cookies from 'js-cookie';

export default {

  data() {
    return {
      baseUrl: 'http://localhost:5000',
      loginForm: {
        username: '',
        password: '',
      },
      registerForm: {
        username: '',
        password: '',
        cell: '',
      },
      registerDialogVisible: false,
    };
  },
  methods: {
    // 登录
    async login() {
      try {
        const { data } = await axios.post(this.baseUrl + `/user/login`, this.loginForm, {
          headers: { 'Content-Type': 'application/json' },
        });
        if (data.message === '登录成功') {
          this.$message.success('登录成功');
          store.commit('setUser', data.user_info);
          localStorage.setItem('user_info', JSON.stringify(data.user_info));

          // 从状态中获取存储用户信息
          const user_info = store.state.user;
          console.log("用户信息:", user_info);

          localStorage.setItem('token', data.token);
          //将令牌保存为有效期为7天的cookie
          Cookies.set('token', this.loginForm.username+12345, { expires: 7 });

          this.$router.push('/monitor');
          // 保存当前时间戳
          const timestamp = Date.now();
          localStorage.setItem('loginTimestamp', timestamp);

        } else {
          this.$message.error(`登录失败: ${data.error}`);
        }
      } catch (error) {
        this.$message.error(`登录失败: ${error.message}`);
      }
    },

    openRegisterDialog() {
      this.registerDialogVisible = true;
    },
    returnLogin() {
      this.registerDialogVisible = false;
    },
    // 注册
    async register() {
      try {
        const response = await axios.post(this.baseUrl + `/user/register`, this.registerForm, {
          headers: { 'Content-Type': 'application/json' },
        });
        const { data } = response;
        if (data.state === 0) {
          this.$message.success('注册成功！！！');
          this.registerDialogVisible = false;
        } else if (data.state === -1) {
          this.$message.error(`注册失败: ${data.msg}`);
        }
      } catch (error) {
        this.$message.error(`注册失败: ${error.message}`);
      }
    },

  },
};
</script>

<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
}

.login-form {
  width: 300px;
}

.register-form {
  width: 100%;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url(../static/jpg/img29.jpg); /* Replace with the path to your image */
  background-size: 100% 100%; /* Adjust as needed */
  background-position: center; /* Adjust as needed */
}

.login-form {
  width: 300px;
}

.register-form {
  width: 100%;
}
.el-form-item label, .el-input__inner {
  color: black;
}
</style>
