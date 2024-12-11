<script setup lang="ts">
import {  RouterView } from 'vue-router'

import { ref } from 'vue'


const activeIndex = ref('extract')




function handleSelect() {

}



</script>

<template>
  <el-container>
    <el-header >
      <el-row >
        <el-col :xl="20" :offset="0" :lg="18">
          
          <!-- <div class="webTitle"><span class="first">S</span>cientific <span class="first">L</span>iterature <span class="first">M</span>anagement <span class="first">P</span>latform</div> -->
          <div class="webTitle"><span class="first">R</span>esearch more, <span class="first">S</span>earch less</div>
          <!-- <div class="titleTip">research more, search less</div> -->
        </el-col>
        <el-col :xl="4" :offset="0" :lg="6">
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect"
            :router="true">
            <el-menu-item index="extract">内容分析</el-menu-item>
             <el-menu-item index="agent">科研助手</el-menu-item>
            <!-- <el-menu-item index="dataset">数据集</el-menu-item>  -->
          </el-menu>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <!-- Main content -->
      <RouterView />

    </el-main>
    <el-footer style="height: 0;">
      <!-- Footer content -->

    </el-footer>

  </el-container>
  
</template>

<style scoped>
.el-main {
  padding-top: 10px;
  padding-bottom: 0;
}
.webTitle {
  height: 50px;
  font-size: 2em;
  line-height: 50px;
 font-family: '华文彩云';
}
.el-menu-item {
  height: 50px;
}
.titleTip {
  text-align: center;
}
</style>
