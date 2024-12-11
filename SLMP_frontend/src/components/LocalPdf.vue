<template lang="">
    <div>
        <el-col :xl="4" :lg="5" :offset="0" style="border: 0.5px solid rgba(0, 0, 0, 0.194); padding: 10px;">
            <el-row :gutter="0" style="" class="paperListHeader">
                <el-col :xl="10" :offset="0" :lg="9">
                    <h2>个人文档</h2>
                </el-col>

                <el-col :xl="4" :lg="5" :offset="0">
                    <el-upload class="upload-demo" :action=fileUploadUrl :show-file-list=false
                        :on-success="fileUploadSuccess" :before-upload="beforeAvatarUpload">
                        <el-button type="primary">上传</el-button>

                    </el-upload>
                </el-col>
                <el-col :xl="4" :lg="5" :offset="0">
                    <el-button type="primary" @click="refreshList">刷新</el-button>
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :xl="10" :offset="0" :lg="9"></el-col>
                <el-col :xl="10" :lg="12" :offset="0">
                    <el-input v-model="pdfName" placeholder="文件名称" clearable @change=""></el-input>

                </el-col>
                <el-col :xl="3" :lg="3" :offset="0">
                    <el-button :icon="Search" circle @click="fetchUserFileList" />
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="24" :offset="0">
                    <el-divider style="margin: 10px 0;"></el-divider>
                </el-col>

            </el-row>


            <el-row :gutter="0">
                <el-col :xl="24" :offset="0">
                    <el-scrollbar>
                        <ul class="paperUl">
                            <li v-for="(td, index) in paperFileList" :key=index :class="{ active: td.isActive }">
                                <div class="name"><span @click="handleFileSelect(td.id, index)">{{ td.name }}</span> <el-tag
                                        :type=td.status class="mx-1" effect="plain" round>
                                        {{ td.statusDesc }}
                                    </el-tag></div>
                                <div>Tags：<el-tag v-for="item in td.tags" effect="dark">{{ item }}</el-tag>
                                    <span class="date">{{ td.gmtModified }}</span>
                                </div>

                                <div class="handleBtn">
                                    <el-row>
                                        <el-col :xl="17" :lg="17" :offset="0"></el-col>
                                        <el-col :xl="5" :lg="5" :offset="0">
                                            <el-button type="primary" round @click=handleFileProcess(index)>{{
                                                td.selectBtnDesc }}</el-button>
                                        </el-col>
                                    </el-row>
                                </div>

                            </li>
                        </ul>
                    </el-scrollbar>

                </el-col>
            </el-row>
            <el-row :gutter="0" class="pagerow">
                <el-col :lg="10" :xl="5" :offset="0"></el-col>

                <el-col :lg="10" :offset="0">
                    <el-pagination background layout="prev, pager, next" :page-size="pageSize" :total="paperTotal"
                        :current-page="currentPage" @current-change="handlePageChange" />
                </el-col>

            </el-row>

        </el-col>
    </div>
</template>
<script setup lang="ts">

</script>
<style scoped>
    
</style>