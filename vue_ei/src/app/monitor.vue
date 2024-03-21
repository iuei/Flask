<template>
  <div>
    <!-- 行，设置间隔为20 -->
    <el-row :gutter="20">
      <!-- 六个订单信息卡片 -->
      <div class="num">
        <el-card :shadow="'hover'" v-for="item in countData" :key="item.name" :body-style="{ display: 'flex', padding: 0 }" class="OrderCard">
          <i class="icon" :class="'el-icon-' + item.icon" :style="{ background: item.color }"></i>
          <div>
            <p class="important-font">￥{{ item.value }}</p>
            <p class="secondary-font">{{ item.name }}</p>
          </div>
        </el-card>
      </div>

      <!-- 柱状图 -->
      <el-card style="height: 300px">
        <div style="height: 300px;" ref="barEcharts">{{ initBarEcharts() }}</div>
      </el-card>
      <!-- 饼图和日历 -->
      <div class="num graph">
        <el-card style="width: 34%; height: 340px; margin-right: 1%">
          <div style="width: 100%; height: 350px;" ref="pieEcharts">{{ initPieEcharts() }}</div>
        </el-card>
        <el-card style="width: 65%; height: 340px">
          <div style="height: 265px">
            <el-calendar v-model="value"></el-calendar>
          </div>
        </el-card>
      </div>
    </el-row>
  </div>
</template>


<script>
// 引入echarts库
import * as echarts from 'echarts';

export default {
  name: "Index",
  data() {
    return {
      // 日期选择器的值
      value: new Date(),

      // 订单统计数据
      countData: [
        {name: '新增用户', value: 1200, icon: 'success', color: '#2ec7c9'},
        {name: '购买人数', value: 1200, icon: 'star-on', color: '#ffb980'},
        {name: '今日支付订单', value: 1200, icon: 's-goods', color: '#5ab1ef'},
        {name: '今日退款订单', value: 1200, icon: 'success', color: '#2ec7c9'},
      ]
    }
  },
  methods: {
    // 初始化柱状图
    initBarEcharts() {
      // 创建一个Promise对象
      let p = new Promise((resolve) => {
        resolve()
      })

      // 异步执行echarts的初始化函数
      p.then(() => {
        // 获取echarts图表展示DOM
        let myChart = echarts.init(this.$refs.barEcharts)
        let option = {
          title: {
            text: '销售表'
          },
          tooltip: {},
          legend: {
            data: ['今日销量', '昨日销量']
          },
          xAxis: {data: ['咖啡', '奶制品', '水', '方便面', '水果', '饮料']},
          yAxis: {},
          series: [
            {name: '今日销量', type: 'bar', data: [5, 20, 36, 10, 10, 20]},
            {name: '昨日销量', type: 'bar', data: [10, 18, 34, 8, 12, 21]}
          ]
        }
        // 使用指定的配置项和数据显示图表
        myChart.setOption(option);
      })
    },
    // 初始化饼图
    initPieEcharts() {
      let p = new Promise((resolve) => {
        resolve()
      })

      // 异步执行echarts的初始化函数
      p.then(() => {
        let myChart = echarts.init(this.$refs.pieEcharts);
        let option = {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '0%',
            left: 'left'
          },
          series: [
            {
              name: '用户数据',
              type: 'pie',
              radius: ['20%', '65%'],
              avoidLabelOverlap: false,
              label: {
                show: false,
                position: 'left'
              },
              labelLine: {
                show: false,
              },
              data: [
                { value: 1000, name: '会员' },
                { value: 735, name: '普通用户' },
                { value: 580, name: '男' },
                { value: 484, name: '女' },
                { value: 10, name: '预购量' }
              ]
            }
          ]
        }
        // 使用指定的配置项和数据显示图表
        myChart.setOption(option);
      })
    }
  }
}
</script>


<style lang="less" scoped>
.important-font{
  font-weight: 900;
  font-size: 25px;
}
.secondary-font{
  color: #909399;
}

.OrderCard{
  margin: 0 0 30px 30px;
  border: #DCDFE6 1px solid;
  border-radius: 10px;
  i{
    width: 30%;
    line-height: 120px;
    font-size: 30px;
    color:#fff
  }
  div{
    width: 300px;
  }
}
.el-card{
  border: none;
}
.num{
  display: flex;
  flex-wrap: wrap;
}
.graph{
  margin: 15px 0 0 0;
}
.el-calendar{
  height: 265px ;
}
</style>
