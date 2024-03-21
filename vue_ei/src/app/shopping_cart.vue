<template>
  <div>
    <el-row>
      <!-- 搜索栏 -->
      <el-row class="search-bar" style="justify-content: space-between; align-items: center;">
        <el-form :model="commodity" inline>
          <el-form-item label="编号">
            <el-input v-model="commodity.serial" style="width: 300px;"></el-input>
          </el-form-item>
          <el-form-item label="名称">
            <el-input v-model="commodity.name" style="width: 300px;"></el-input>
          </el-form-item>
          <el-button type="primary" @click="search">查询</el-button>
        </el-form>
      </el-row>
      <!-- 左侧表格，宽度为70% -->
      <el-table :data="commodity.tableData" stripe border style="width: 70%;">
        <!-- 表格列 -->
        <el-table-column prop="serial" label="编号" width="150"/>
        <el-table-column prop="name" label="名称"/>
        <el-table-column prop="price" label="价格"/>
        <el-table-column prop="inventory" label="库存"/>
        <el-table-column prop="type" label="类型"/>
        <el-table-column prop="address" label="操作" width="180" class="operate">
          <template slot-scope="scope">
            <el-button type="text" @click="openInfo(scope.row)">添加至购物车</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
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
    </div>
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
      total:0,
      current_page:1,
      page_sizes:[10,20,30,40],
      page_size:11,

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

    };
  },

  created() {
    this.search();
  },

  methods: {
    // 加载/查询数据
    search() {
      try {
        axios.post(this.baseUrl + `/commodity/search`, {
          serial: this.commodity.serial,
          name: this.commodity.name,
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
  },
};
</script>

<style scoped>

</style>
