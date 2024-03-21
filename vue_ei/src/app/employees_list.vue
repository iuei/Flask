<template>
  <el-table :data="list" stripe border style="width: 100%">
    <el-table-column prop="id" label="编号" width="180"/>
    <el-table-column prop="name" label="名称" width="180"/>
    <el-table-column prop="number" label="手机号"/>
    <el-table-column prop="salary" label="薪资"/>
    <el-table-column prop="title" label="职位"/>
    <el-table-column prop="date" label="创建日期"/>
    <el-table-column prop="address" label="操作" width="180" class="operate">
    </el-table-column>
  </el-table>
</template>

<script>
import axios from "axios";

export default {
  name:'employees',

  data(){
    return{
      baseUrl:'http://localhost:5000',
      list:[],
    }
  },
  created() {
    this.search();
  },

  methods:{
    search() {
      axios.post(this.baseUrl + '/employees/load')
          .then(response => {
            this.list = response.data;
          })
          .catch(error => {
            console.error("信息获取失败", error.response);
          });
    },


  }
}
</script>

<style scoped>

</style>
