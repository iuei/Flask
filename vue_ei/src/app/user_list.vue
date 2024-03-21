<template>
  <el-row>
    <el-row>
    <el-select v-model="type" aria-label="用户类型" placeholder="请选择"  @change="fetchTableData">
      <el-option label="全部" value="100"></el-option>
      <el-option label="普通用户" value="1"></el-option>
      <el-option label="会员" value="2"></el-option>
      <el-option label="管理员" value="3"></el-option>
    </el-select>
    <el-table :data="userList" stripe border style="width: 100%">
      <el-table-column prop="id" label="ID" width="180"/>
      <el-table-column prop="username" label="名称" width="180"/>
      <el-table-column prop="cell" label="手机号" width="180"/>
      <el-table-column prop="sex" label="性别"/>
      <el-table-column prop="address" label="地址"/>
      <el-table-column prop="user_type" label="用户类型"/>
      <el-table-column prop="balance" label="余额"/>
      <el-table-column prop="text" label="操作">
        <template  slot-scope="scope">
          <el-button type="text" @click="openInfo(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="add_dialog_visible" title="编辑用户数据" :close-on-click-modal="false" center>
      <el-form :model="edit_user" label-width="125">
        <el-form-item label="名称" prop="username">
          <el-input type="text" v-model="edit_user.username" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="cell">
          <el-input type="text" v-model="edit_user.cell" placeholder="请输入编号" disabled></el-input>
        </el-form-item>
        <el-select v-model="edit_user.sex" label="性别">
          <el-option value="男"></el-option>
          <el-option value="女"></el-option>
        </el-select>
        <el-form-item label="地址" prop="address">
          <el-input type="text" v-model="edit_user.address" placeholder="请输入编号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-select v-model="edit_user.user_type" label="用户类型">
            <el-option
                v-for="(item, index) in edit_user_type"
                :key="index"
                :label="item.label"
                :value="item.value"
            ></el-option>
          </el-select>

        </el-form-item>
        <el-form-item label="余额" prop="balance">
          <el-input type="text" v-model="edit_user.balance" placeholder="请输入编号"></el-input>
        </el-form-item>
        <el-form-item class="text-center">
          <el-button class="el-button--medium" type="primary" @click="edit">保存</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </el-row>
    <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :current-page.sync="current_page"
        :page-sizes="page_sizes"
        :page-size.sync="page_size"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
    ></el-pagination>
  </el-row>
</template>

<script>
import axios from "axios";

export default {
  name: 'user',

  data() {
    return {
      total: 0,
      current_page: 1,
      page_sizes: [10, 20, 30, 40],
      page_size: 12, //页
      add_dialog_visible: false,
      elForm: {},
      baseUrl: 'http://localhost:5000',
      userList: [],
      edit_user: [],
      user_search: {},
      type:'100',
      edit_type: '1',
      edit_user_type: [
        {'label': '普通用户', 'value': 1},
        {'label': '会员', 'value': 2},
        {'label': '管理员', 'value': 3}
      ],
      selectedOption: [
        {'label': '普通用户', 'value': 1},
        {'label': '会员', 'value': 2},
        {'label': '管理员', 'value': 3}
      ]
    };
  },

  created() {
    this.fetchTableData();
  },

  methods: {
    fetchTableData() {
      axios.get(`${this.baseUrl}/user/info`, {
        params: {
          page: this.current_page,
          page_size: this.page_size,
          user_type:this.type
        }
      })
          .then(response => {
            this.userList = response.data.user_data;
            this.total = response.data.total;
            this.current_page = response.data.current_page;
            this.page_size = response.data.page_size;
          })
          .catch(error => {
            console.error('Error fetching user data:', error);
          });
    },

    openInfo(row) {
      if (row) {
        this.edit_user = {
          id: row.id,
          username: row.username,
          cell: row.cell,
          sex: row.sex,
          address: row.address,
          user_type: row.user_type,
          balance: row.balance,
        };
        this.add_dialog_visible = true;
      }
    },
    edit() {
      axios.post(this.baseUrl + `/user/edit/` + this.edit_user.id, this.edit_user)
          .then(response => {
            this.$message.success('编辑成功')
            // 可选：关闭对话框或在成功后执行其他操作
            this.add_dialog_visible = false;
            this.fetchTableData(); // 编辑后刷新表格数据
          })
          .catch(error => {
            console.error('用户编辑时出错:', error);
            // 根据需要处理错误
          });
    },
    handleSizeChange(page_size) {
      this.page_size = page_size;
      this.fetchTableData();
    },

    handleCurrentChange(currentPage) {
      this.current_page = currentPage;
      this.fetchTableData();
    },

  },
};
</script>

<style scoped>
.test-right {
  text-align: right;
}

.text-center {
  text-align: center;
}
</style>
