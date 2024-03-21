<template>
  <el-row>
    <!-- 搜索栏 -->
    <el-row class="search-bar" style="justify-content: space-between; align-items: center;">
      <el-form :model="commodity" inline>
        <el-form-item label="编号">
          <el-input v-model="commodity.serial" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="commodity.name" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search_status" @change="search">
            <el-option v-for="(item,index) in search_status_data" :label="item.label" :key="index" :value="item.value" ></el-option>
          </el-select>
        </el-form-item>
        <el-button type="primary" @click="search">查询</el-button>
        <el-form-item>
<!--          <download-excel-->
<!--              :fields = "json_fields"-->
<!--              @click = "downloadList"-->
<!--              name = "订单数据.xls">-->
<!--            <el-button type="success" >导出excel</el-button>-->
<!--          </download-excel>-->
        </el-form-item>
        <el-button class="test-right" type="success" @click="add_dialog_visible = true">添加商品</el-button>
      </el-form>
    </el-row>

    <!-- 添加弹窗 -->
    <el-dialog :visible.sync="add_dialog_visible" title="添加商品" :close-on-click-modal="false">
      <el-form :model="add_list" ref="ruleForm" label-width="200" class="demo-ruleForm">
        <!-- 添加数据的表单项 -->
        <el-form-item label="编号" prop="name">
          <el-input type="text" v-model="add_list.serial" placeholder="请输入编号"></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input type="text" v-model="add_list.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input type="text" v-model="add_list.price" placeholder="请输入价格"></el-input>
        </el-form-item>
        <el-form-item label="库存" prop="price">
          <el-input type="text" v-model="add_list.inventory" placeholder="请输入库存"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-input type="text" v-model="add_list.type" placeholder="请输入类型"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="add_list.status" active-text="上架" active-value="1" inactive-color="下架" inactive-value="2"></el-switch>
        </el-form-item>

        <!-- 弹窗中的操作按钮 -->
        <el-row style="text-align: center;">
          <el-button type="primary" @click="add">立即添加</el-button>
          <el-button @click="add_dialog_visible = false">取消</el-button>
        </el-row>
      </el-form>
    </el-dialog>

    <!-- 编辑弹窗 -->
    <el-dialog :visible.sync="edit_dialog_visible" title="编辑数据" :close-on-click-modal="false" center>
      <el-form :model="edit_list" ref="editForm" label-width="150" class="demo-ruleForm">
        <!-- 编辑数据的表单项 -->
        <el-form-item label="编号" prop="type">
          <el-input type="text" v-model="edit_list.serial" disabled></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input type="text" v-model="edit_list.name"></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input type="text" v-model="edit_list.price"></el-input>
        </el-form-item>
        <el-form-item label="库存" prop="inventory">
          <el-input type="text" v-model="edit_list.inventory"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-input type="text" v-model="edit_list.type"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="edit_list.status" active-text="上架" active-value="1" inactive-color="下架" inactive-value="2"></el-switch>
        </el-form-item>

        <!-- 弹窗中的操作按钮 -->
        <el-row style="text-align: center;">
          <el-button type="primary" @click="edit">保存</el-button>
          <el-button @click="edit_dialog_visible = false">取消</el-button>
        </el-row>
      </el-form>
    </el-dialog>

    <!-- 表格 -->
    <el-table :data="commodity.tableData" stripe border style="width: 100%">
      <!-- 表格列 -->
      <el-table-column prop="serial" label="编号" width="180"/>
      <el-table-column prop="name" label="名称" width="180"/>
      <el-table-column prop="price" label="价格" width="180"/>
      <el-table-column prop="inventory" label="库存"/>
      <el-table-column prop="type" label="类型"/>
      <el-table-column prop="status" label="状态"/>
      <el-table-column prop="create_time" label="创建日期"/>
      <el-table-column prop="address" label="操作" width="180" class="operate">
        <template slot-scope="scope">
          <el-button type="text" @click="openInfo(scope.row)">编辑</el-button>
          <el-button type="text" @click="del(scope.row.id)" style="color: #F56C6C" >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
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
  name: 'commodity_list',

  data() {
    return {
      loading: false,
      row: null,
      baseUrl: 'http://localhost:5000',
      edit_dialog_visible: false,
      add_dialog_visible: false,
      total:0,
      current_page:1,
      page_sizes:[10,20,30,40],
      page_size:11,
      json_fields: {
        '编号': 'serial',
        '名称': 'name',
        '价格': 'price',
        '库存': 'inventory',
        '类型': 'type',
        '状态': 'status',
        '创建日期': 'create_time',
      },
      commodity: {
        serial: '',
        name: '',
        type: '',
        price: '',
        inventory: '',
        status: '1',
        tableData: [],
        id:'',
      },
      search_status:100,
      search_status_data:[
        {'label': '所有', 'value': 100},
        {'label': '上架', 'value': 1},
        {'label': '下架', 'value': 2}
      ],
      add_list:{
        serial: '',
        name: '',
        type: '',
        price: '',
        inventory: '100',
        status: '1',
        tableData: [],
        id:'',
      },
      edit_list: {
        name: '',
        type: '',
        price: '',
        serial: '',
        inventory: '',
        status: '1',
      },
    };
  },

  created() {
    this.search();
  },

  methods: {
    // 添加数据
    add() {
      try {
        this.$refs.ruleForm.validate().then(() => {
          axios.post(this.baseUrl + `/commodity/add`, this.add_list)
              .then(response => {
                if (response.status === 200 && response.data.success) {
                  // 添加成功
                  this.$message.success('添加成功');
                  this.search();
                  this.add_dialog_visible = false;
                  this.clearFormFields('add_list');
                } else {
                  // 添加失败
                  this.$message.error('添加失败',response.data.msg);
                  this.add_dialog_visible = false;
                }
              })
              .catch(error => {
                this.$message.error('添加失败',response.data.error);
                this.add_dialog_visible = false;
              });
        });
      } catch (error) {
        this.handleApiError(error, '添加失败');
      }
    },
    // 基于原始数据编辑
    openInfo(row) {
      if (row) {
        this.edit_list = {
          id: row.id,
          inventory: row.inventory,
          serial: row.serial,
          status: '1',
          name: row.name,
          type: row.type,
          price: row.price,
        };
        this.edit_dialog_visible = true;
      }
    },
    // 编辑数据
    edit() {
      try {
        this.$refs.editForm.validate().then(() => {
          axios.post(this.baseUrl+`/commodity/edit`, this.edit_list)
              .then(response => {
                if (response.data.state === 0) {
                  this.$message.success('编辑成功');
                  this.edit_dialog_visible = false;
                  this.search();
                  this.clearFormFields('edit_list');
                } else {
                  this.$message.error('编辑失败');
                }
              })
              .catch(error => {
                this.handleApiError(error, '编辑失败');
              });
        });
      } catch (error) {
        this.handleApiError(error, '编辑失败');
      }
    },
    // 加载/查询数据
    search() {
      try {
        axios.post(this.baseUrl + `/commodity/search`, {
          serial: this.commodity.serial,
          name: this.commodity.name,
          status: this.search_status,
          page: this.current_page,
          page_size: this.page_size
        })
            .then(response => {
              this.commodity.tableData = response.data.data;
              this.total = response.data.total;
              this.current_page = response.data.current_page;
              this.page_size = response.data.page_size;
            })
            .catch(error => {
              this.handleApiError(error, '查询失败');
            });
      } catch (error) {
        this.handleApiError(error, '查询失败');
      }
    },
// 打印excel表
    async downloadList() {
      const parameter = {
        // 每页数量
        serial: this.commodity.serial,
        name: this.commodity.name,
        price: this.commodity.price,
        inventory: this.commodity.inventory,
        type: this.commodity.type,
        status: this.commodity.status,
        create_time: this.commodity.create_time,
      }
      this.loading = true
      await axios.post(this.baseUrl+`/commodity/print`, parameter).then(res => {
        if (res.data.state === 0) {
          this.download_data = res.data.data
        } else {
          this.tableData = []
          this.$alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            callback: action => {
            }
          })
        }
        this.loading = false
      }).catch(() => {
        this.tableData = []
        this.$alert('网络异常', '提示', {
          confirmButtonText: '确定',
          callback: action => {
          }
        })
        this.loading = false
      })
      return this.download_data
    },

// 删除商品方法，接收商品ID作为参数
    del(id) {
      // 使用确认对话框询问用户是否确定删除当前商品
      this.$confirm('是否删除当前商品', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 用户点击确定后，发起删除商品的请求
        axios.post(this.baseUrl + '/commodity/delete', { 'id': id })
            .then(res => {
              // 根据服务器返回的状态进行处理
              if (res.data.state === 0) {
                // 删除成功，显示成功提示，然后执行搜索方法刷新商品列表
                this.$message.success('删除成功');
                this.search();
              } else {
                // 删除失败，显示错误提示
                this.$alert(res.data.msg, '提示', {
                  confirmButtonText: '确定',
                  callback: action => {
                    // 可以在用户点击确定后执行一些操作
                  }
                });
              }
              this.loading = false;
            })
            .catch(() => {
              // 请求失败，显示网络异常提示
              this.$alert('网络异常', '提示', {
                confirmButtonText: '确定',
                callback: action => {
                  // 可以在用户点击确定后执行一些操作
                }
              });
              this.loading = false;
            });
      }).catch(() => {
        cancelButtonText:'取消'
        this.edit_dialog_visible = false
        // this.$message.info('取消删除');
      });
    },


    // 注销账户重定向到登录页面
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
      this.$message.success('注销成功');
    },

    handleSizeChange(current_page) {
      this.current_page = current_page
      this.search();
    },

    handleCurrentChange(page_size) {
      this.page_size = page_size;
      this.search();
    },

    handleApiError(error, message) {
      console.error(message, error);
      if (error.response) {
        console.log('Response:', error.response);
      }
    },

    clearFormFields(formName) {
      this[formName] = {};
    },
  },
};
</script>

<style scoped>
.test-right {
  text-align: right;
}

</style>
