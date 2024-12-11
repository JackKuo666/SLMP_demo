<template>
    <div class="onlinePdfs">
        <el-row :gutter="0">
            <el-col :span="12" :offset="1">
                <h2>必读论文</h2>
            </el-col>
            <el-col :span="10" :offset="0">
                <el-autocomplete v-model="qKey" :fetch-suggestions="querySearch" :trigger-on-focus="false" clearable
                    class="inline-input" placeholder="关键词搜索" @select="autoCompleteSelect" style="width: 100%;" />
            </el-col>
            <el-col :span="1" :offset="0">
                <el-button :icon="Search" circle @click="queryKeyword" />
            </el-col>
            
        </el-row>
        <el-row :gutter="0">
            <el-col :span="24" :offset="0">
                <el-divider style="margin: 10px 0;"></el-divider>
            </el-col>
        </el-row>
        <el-row :gutter="0">
            <el-col :span="24" :offset="0">
                <div class="paper" v-for="(item, index) in paperList" :key="index">
                    <div class="title"><span @click="$emit('chooseOnlinePaper', item, currentPage, pageSize, qKey)">{{ item.title }}</span>
                        <el-button class="addTolocal" type="primary" plain @click=addToLocal(item)>+加入个人文档</el-button>
                    </div>
                    <div class="author">{{ item.authors }}</div>
                    <span class="tag" v-for="(t, i) in item.tags" :key="i">
                        <el-tag type="success" size="" effect="plain">{{ t }}</el-tag>
                    </span>
                    <div class="abstract">{{ item.abstract }}</div>
                </div>
            </el-col>

        </el-row>
        <el-pagination background layout="prev, pager, next" :page-size="pageSize" :total="paperTotal"
                    :current-page="currentPage" @current-change="handlePageChange" style="float: right;" />


    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { queryEsByKey, pageEs, addOnline } from '@/api/onlinePaper'
import { type Paper, type LinkItem } from '@/api/commonType'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'


const emit = defineEmits(['addTolocalSuccess'])
const qKey = ref('')


const currentPage = ref(1)
const pageSize = ref(10)
const paperTotal = ref(0)
const paperList = ref<Paper[]>([])
function handlePageChange(value: number) {
    currentPage.value = value
    queryKeyword()
}
const links = ref<LinkItem[]>([])

const querySearch = (queryString: string, cb: any) => {
    queryEsByKey(queryString).then(response => {
        let resultList = response.data.data
        let temp: LinkItem[] = []
        resultList.forEach((r: any) => {
            temp.push({
                value: r['title'],
                link: r['id']
            })
        })
        links.value = temp
        let results = queryString
            ? links.value.filter(createFilter(queryString))
            : links.value
        cb(results)
    })


}
const createFilter = (queryString: string) => {
    return (restaurant: LinkItem) => {
        return (
            restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) > -1
        )
    }
}
const autoCompleteSelect = (item: LinkItem) => {
    console.log(item)
}

function addToLocal(paper: Paper) {
    addOnline(paper).then(response => {
        let result = response.data.data
        if (result === true) {
            ElMessage({
                message: '添加成功',
                type: 'success'
            })
            emit('addTolocalSuccess')
        } else {
            ElMessage({
                message: '添加失败，请重新添加',
                type: 'error'
            })
        }
    })
}
function queryKeyword() {
    pageQuery(qKey.value)
}
function pageQuery(keyword: string) {
    pageEs((currentPage.value-1) * pageSize.value, pageSize.value, keyword).then(response => {
        console.log(response.data.data)
        
        let results = response.data['hits']
        let tempList:Paper[] = [] 
        results.forEach((r:any) => {
            let source = r['_source']
            tempList.push({
                id: r['_id'],
                title:source['title'],
                authors:source['authors'],
                url:"",
                abstract:source['abstract'],
                tags:[],
                metas:[]
            })
        });
        paperList.value = tempList
        paperTotal.value = response.data['total']['value']/pageSize.value

    })
}
onMounted(() => {
    pageQuery("")
})
</script>
<style scoped>
.onlinePdfs {
    height: 90vh;
    overflow: auto;
}

.paper {
    margin: 10px 5px;
    padding: 10px;
    border: 1px solid transparent;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px;
    border-radius: 30px;
    opacity: 0.75;
    transition: all 100ms ease-in 0s;
    background-color: rgb(247, 249, 252);
}

.paper .title {
    color: rgb(59, 68, 214);
    font-size: 24px;
    font-weight: 500;
    line-height: 1.2;
    margin-bottom: 10px;
    text-decoration: none;

}

.paper .title .addTolocal {
    margin-left: 10px;
}

.paper .title:hover {
    cursor: pointer;
    color: blue;
}

.paper .abstract {
    font-size: 16px;
    color: rgba(0, 0, 0, 0.45);
}

.el-autocomplete {
    width: 100%;
}
</style>