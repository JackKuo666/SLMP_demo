<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { pageUserFile, handlePaperFile, getFileUrl } from '@/api/paperExtract'
import { baseUrl } from '@/config/env'
import { ElMessage, ElMessageBox } from 'element-plus'
import PdfAbstract from '@/components/PdfAbstract.vue'
import PdfOa from '@/components/PdfQa.vue'
import PdfViewer from '@/components/PdfViewer.vue'
import OnlinePdf from '@/components/OnlinePdf.vue'
import type { UploadProps } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { queryEsByKey, pageEs } from '@/api/onlinePaper'
import { type Paper, type PaperFileType, type LinkItem, type metaType } from '@/api/commonType'

const fileUploadUrl = baseUrl + "/kodata/userextractfile/upload"
const onlinePaperList = ref<Paper[]>([])
const paperFileList = ref<PaperFileType[]>([])
const pdfAbstractDom: any = ref(null)
const pdfViewDom: any = ref(null)
const pdfQaDom: any = ref(null)
const oldSelectPaper = ref<PaperFileType>()
const pdfsrc = ref("/img/HelloWorld.pdf")
const activeName = ref("abstract")
const currentPage = ref(1)
const pageSize = ref(10)
const paperTotal = ref(0)
const olCurrentPage = ref(1)
const olPageSize = ref(10)
const olPaperTotal = ref(0)
const pdfName = ref("")
const showPdf = ref(false)
const paperTab = ref('local')
const qkey = ref('')
const domainMetaList = ref<metaType[]>([{
    fileId: 1,
    metaKey: "number_of_mags",
    metaValue: "871"
},
{
    fileId: 1,
    metaKey: "Is it a new sample",
    metaValue: "yes"
},
{
    fileId: 1,
    metaKey: "data  available at",
    metaValue: "PRJNA434545 (Additional file 4)"
}, {
    fileId: 1,
    metaKey: "data can be found in",
    metaValue: "https://figshare.com/s/7684627445e3621aba24"
}]);
function refreshList() {
    fetchUserFileList();
}
function fetchUserFileList() {
    pageUserFile({ current: currentPage.value, size: pageSize.value, name: pdfName.value }).then((response: any) => {
        let retData = response.data.data
        paperFileList.value = retData.records;
        pageSize.value = retData.size
        paperTotal.value = retData.total
        currentPage.value = retData.current
        paperFileList.value.forEach(d => {
            if (oldSelectPaper.value != undefined && d.id == oldSelectPaper.value.id) {
                d.isActive = true
            }
            if (d.isExtract == 'P') {
                d.status = ''
                d.statusDesc = '处理中'
                d.selectBtnDesc = "处理中"
            } else if (d.isExtract == 'Y') {
                d.status = 'success'
                d.statusDesc = "处理成功"
                d.selectBtnDesc = '重新处理'
            } else if (d.isExtract == 'N') {
                d.status = 'info'
                d.statusDesc = '未处理'
                d.selectBtnDesc = '开始处理'
            } else if (d.isExtract == 'F') {
                d.status = 'danger'
                d.statusDesc = '处理失败'
                d.selectBtnDesc = '重新处理'
            }
            d.tags = d.tag == null ? null : (d.tag.split(','))
        })
    })
}
function handleFileSelect(fileId: string, index: number) {
    showPdf.value = true

    pdfAbstractDom.value.fetchMeta(fileId)
    let currentPaper = paperFileList.value[index]

    if (oldSelectPaper.value != null) {
        oldSelectPaper.value.isActive = false
    }
    oldSelectPaper.value = currentPaper
    currentPaper.isActive = true
    if (currentPaper.pdfUrl != null) {
        pdfsrc.value = currentPaper.pdfUrl
        pdfViewDom.value.loadPdf(currentPaper.pdfUrl)
        return
    }
    getFileUrl(fileId).then(response => {
        let result = response.data.data
        currentPaper.pdfUrl = result
        pdfsrc.value = result;
        pdfViewDom.value.loadPdf(result)
    })
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
function handleFileProcess(index: number) {

    if (paperFileList.value?.length == 0) {
        return;
    }
    const fileInfo = paperFileList.value[index]
    if (fileInfo.isExtract == 'P') {
        ElMessage({
            message: '该文件正在处理中，请耐心等待',
            type: 'info'
        })
    } else if (fileInfo.isExtract == 'Y' || fileInfo.isExtract == 'F') {
        ElMessageBox.confirm(
            '是否重新处理该文件？',
            'Warning',
            {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning',
            }
        )
            .then(() => {
                handlePaperFile(fileInfo.id);
                fetchUserFileList()
            })
            .catch(() => {

            })
    } else if (fileInfo.isExtract == 'N') {
        ElMessageBox.confirm(
            '是否开始处理该文件？',
            'Warning',
            {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning',
            }
        )
            .then(() => {
                handlePaperFile(fileInfo.id);
            })
            .catch(() => {

            })
    }
}
function fileUploadSuccess() {
    fetchUserFileList();
}
const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {

    if (rawFile.type !== 'application/pdf') {
        ElMessage.error('当前仅支持PDF文件')
        return false
    } else if (rawFile.size / 1024 / 1024 > 10) {
        ElMessage.error('文件大小需小于10MB!')
        return false
    }
    return true
}
const autoCompleteSelect = (item: LinkItem) => {
    console.log(item)
}

function handlePageChange(value: number) {
    currentPage.value = value
    fetchUserFileList()
}
function showQaPane(pane: any, ev: any) {

    if (pane.props.name == 'qa') {
        console.log("show qa")
        pdfQaDom.value.checkQaStatus(oldSelectPaper.value?.id)
    }

}
function olPage(keyword: string) {
    pageEs((olCurrentPage.value - 1) * olPageSize.value, olPageSize.value, keyword).then(response => {
        console.log(response.data.data)

        let results = response.data['hits']
        let tempList: Paper[] = []
        results.forEach((r: any) => {
            let source = r['_source']
            tempList.push({
                id: r['_id'],
                title: source['title'],
                authors: source['authors'],
                url: "",
                abstract: source['abstract'],
                tags: [],
                metas: []
            })
        });
        onlinePaperList.value = tempList
        olPaperTotal.value = response.data['total']['value'] / olPageSize.value

    })
}
function handleOnlinePaper(paper: Paper) {
    console.log(paper)
    if (showPdf.value == false) {
        showPdf.value = true
        paperTab.value = 'online'
        olPage(qkey.value)
    }

    pdfsrc.value = paper.url
    if (pdfViewDom.value != null) {
        pdfViewDom.value.loadPdf(paper.url)
    }
    pdfAbstractDom.value.showMeta(paper.metas)
}
function chooseOnlinePaper(paper: Paper, page: number, size: number, keyw: string) {
    olCurrentPage.value = page
    olPageSize.value = size
    qkey.value = keyw
    handleOnlinePaper(paper)
}
function addTolocalSuccess() {
    fetchUserFileList()
}
function queryKeyword() {
    olPage(qkey.value)
}
onMounted(() => {
    fetchUserFileList();
})
</script>
<template>
    <el-row>
        <el-col :xl="4" :lg="5" :offset="0" style="border: 0.5px solid rgba(0, 0, 0, 0.194); padding: 10px;"
            class="mainCol">
            <el-tabs class="demo-tabs" v-model="paperTab">
                <el-tab-pane label="个人文档" name="local">
                    <el-row :gutter="0" style="" class="paperListHeader">
                        <el-col :xl="4" :lg="5" :offset="0">
                            <el-upload class="upload-demo" :action=fileUploadUrl :show-file-list=false
                                :on-success="fileUploadSuccess" :before-upload="beforeAvatarUpload">
                                <el-button type="primary">上传</el-button>
                            </el-upload>
                        </el-col>
                        <el-col :xl="4" :lg="5" :offset="0">
                            <el-button type="primary" @click="refreshList">刷新</el-button>
                        </el-col>
                        <el-col :xl="10" :lg="11" :offset="0">
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
                            <div class="paperListDiv">
                                <div class="paper" v-for="(td, index) in paperFileList" :key=index
                                    :class="{ active: td.isActive }">
                                    <div class="title" @click="handleFileSelect(td.id, index)">{{ td.name }}
                                        <el-tag :type=td.status class="mx-1" effect="plain" round>
                                            {{ td.statusDesc }}
                                        </el-tag>
                                    </div>
                                    <div class="author">{{ td.gmtModified }}</div>
                                    <span class="tag" v-for="(t, i) in td.tags" :key="i">
                                        <el-tag type="success" size="small" effect="plain">{{ t }}</el-tag>
                                    </span>
                                    <div class="handleBtn">
                                        <el-row>
                                            <el-col :xl="17" :lg="17" :offset="0"></el-col>
                                            <el-col :xl="5" :lg="5" :offset="0">
                                                <el-button type="primary" round @click=handleFileProcess(index)>{{
                                                    td.selectBtnDesc }}</el-button>
                                            </el-col>
                                        </el-row>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                    <div class="pagerow">
                        <el-pagination background layout="prev, pager, next" :page-size="pageSize" :total="paperTotal"
                            :current-page="currentPage" @current-change="handlePageChange" style="float: right;"
                            :hide-on-single-page="true" />
                    </div>

                </el-tab-pane>
                <el-tab-pane label="必读论文" v-if="showPdf" name="online">
                    <el-row :gutter="0" style="" class="paperListHeader">

                        <el-col :span="22">
                            <el-autocomplete v-model="qkey" :fetch-suggestions="querySearch" :trigger-on-focus="false"
                                clearable class="inline-input w-50" placeholder="关键词搜索" @select="autoCompleteSelect"
                                style="width: 100%;" />
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
                    <div class="paperListDiv">
                        <div class="paper" v-for="(item, index) in onlinePaperList" :key="index">
                            <div class="title" @click="handleOnlinePaper(item)">{{ item.title }}</div>
                            <div class="author">{{ item.authors }}</div>
                            <span class="tag" v-for="(t, i) in item.tags" :key="i">
                                <el-tag type="success" size="" effect="plain">{{ t }}</el-tag>
                            </span>
                        </div>

                    </div>
                    <div class="pagerow">
                        <el-pagination layout="prev, pager, next" :page-size="olPageSize" :total="olPaperTotal"
                            :current-page="olCurrentPage" @current-change="handlePageChange" style="float: right;"
                            :pager-count="6" />
                    </div>
                </el-tab-pane>
                <el-tab-pane label="向量检索"></el-tab-pane>
                <el-tab-pane label="开放数据"></el-tab-pane>
            </el-tabs>
        </el-col>

        <el-col :xl="16" :lg="14" :offset="0" class="mainCol">
            <div v-if="showPdf">
                <PdfViewer :pdfUrl="pdfsrc" ref="pdfViewDom"></PdfViewer>
            </div>
            <div v-if="!showPdf">
                <OnlinePdf @chooseOnlinePaper="chooseOnlinePaper" @addTolocalSuccess="addTolocalSuccess"></OnlinePdf>

            </div>
        </el-col>
        <el-col :xl="4" :lg="5" :offset="0" class="mainCol">
            <el-tabs v-model="activeName" type="card" @tab-click="showQaPane">
                <el-tab-pane label="元数据" name="abstract">
                    <PdfAbstract ref="pdfAbstractDom"></PdfAbstract>
                </el-tab-pane>
                <el-tab-pane label="领域数据" name="dataf">
                    <el-descriptions class="margin-top" :column="1" border>

                        <el-descriptions-item v-for="(item, index) in domainMetaList" :key="index">
                            <template #label>
                                <div class="cell-item">

                                    {{ item.metaKey }}
                                </div>
                            </template>
                            {{ item.metaValue }}
                        </el-descriptions-item>
                    </el-descriptions>
                </el-tab-pane>
                <el-tab-pane label="问答" name="qa">
                    <PdfOa ref="pdfQaDom"></PdfOa>
                </el-tab-pane>

            </el-tabs>
        </el-col>

    </el-row>
</template>
<style scoped>
.mainCol {
    height: calc(100vh - 80px);

}

.el-divider {
    margin: 5px 0;
}

.el-tabs--left .el-tabs__content {
    height: 100%;
}

.paperUl {
    list-style-type: none;
    padding-left: 10px;
}

.paperUl li {
    margin-bottom: 10px;
}


.paperUl li .date {
    float: right;
}

.paperUl .active {
    background-color: aliceblue;
}

.paperListDiv {
    height: calc(100vh - 240px);

    overflow: auto;
    margin-bottom: 5px;
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

    font-weight: 500;
    line-height: 1.2;
    margin-bottom: 10px;
    text-decoration: none;

}

.paper .title:hover {
    cursor: pointer;
}

.pagerow {
    /* position:absolute;
    bottom: 0; */
}

@media (min-width: 1920px) {
    .el-scrollbar {
        height: 900px;
    }
}

@media (max-width:1919px) {
    .el-scrollbar {
        height: 600px;
    }
}</style>