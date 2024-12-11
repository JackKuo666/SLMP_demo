<template >
  <div class="unready" v-if="!showQa">
    <div class="tip" v-if="noChoosePaper">请选择文献以进行问答</div>
    <div class="tip" v-if="!noChoosePaper">知识库还未加载完毕，请耐心等待</div>
    <el-button type="info" size="default" @click="checkStatus" v-if="!noChoosePaper">刷新</el-button>

  </div>
  <div class="pdfqamain" v-if="showQa">
    <div class="middle_key" ref="mainScroll">
      <div v-for="item in qaList">
        <div class="middle_top">
          <div class="fl">
            <!-- <p>{{ item.creationTime }}</p> -->
            <div>{{ item.question }}</div>
          </div>
          <div class="fr"><img src="/img/icon1.png" alt="" /></div>
        </div>

        <div class="middle_box">
          <div class="fr"><img src="/img/robot.png" alt="" /></div>
          <div class="fl">
            <!-- <p>{{ item.replyTime }}</p> -->
            <div>{{ item.answer }}</div>

          </div>
        </div>
      </div>
    </div>
    <div class="middle_list">
      <div class="fl">
        <img src="/img/icon12.png" alt="" /><input type="text" v-model="question" placeholder="询问问题" />
      </div>
      <div class="fr" @click="sendQuestionFunc">
        <span>发送</span><img src="/img/icon3.png" alt="" />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { nextTick, ref } from 'vue'
import { sendQuestion, checkKbStatus } from '@/api/paperExtract'
import { type QaType } from '@/api/commonType'


const fileId = ref("")
const qaList = ref<QaType[]>([])
const mainScroll = ref()
const question = ref("")
const showQa = ref(false)
const noChoosePaper = ref(false)
function checkStatus() {
  checkQaStatus(fileId.value)
}
function checkQaStatus(pdfId: string) {

  if (pdfId == undefined) {
    noChoosePaper.value = true
    return
  }
  if ((fileId.value == "") || (fileId.value != "" && fileId.value != pdfId)) {
    fileId.value = pdfId
    qaList.value = []
  }

  checkKbStatus(pdfId).then(response => {
    console.log(response.data.data)
    showQa.value = response.data.data
  })
}
function sendQuestionFunc() {
  let q = question.value;
  if (q == null || q == '') {
    return
  }
  question.value = ""

  let newQa = {
    question: q,
    answer: ""
  }

  let history: string[][] = []
  qaList.value.forEach(qa => {
    history.push([qa.question, qa.answer])
  })
  qaList.value.push(newQa)
  sendQuestion(q, fileId.value, JSON.stringify(history)).then(response => {
    console.log(response.data.data)
    let qaHis = JSON.parse(response.data.data)
    let newQaList: { question: any; answer: any; }[] = []
    qaHis.forEach((qa: any[]) => {
      newQaList.push({
        question: qa[0],
        answer: qa[1]
      })
    });
    qaList.value = newQaList
    // qaList.value[qSize].replyMsg = response.data.data
    // qaList.value[qSize].replyTime = dayjs().format("YYYY-MM-DD HH:mm:ss")
    nextTick(() => {
      mainScroll.value.scrollTo({ top: mainScroll.value.scrollHeight, behavior: 'smooth' });
    })

  })

}

defineExpose({
  checkQaStatus,
});
</script>
<style scoped>
.pdfqamain {
 
  height: calc(100vh - 135px);
}

.middle_key {
  overflow: auto;
  
  height: calc(100vh - 220px);

}

.middle_key::-webkit-scrollbar {
  display: none;
}

.middle_key .middle_top {
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}

.middle_key .middle_top .fl {
  padding-right: 20px;
  margin-top: 10px;
}

.middle_key .middle_top .fl p {
  text-align: right;
  font-size: 16px;
  font-family: Source Han Sans CN;
  font-weight: 400;
  color: #999999;
}

.middle_key .middle_top .fl div {
  padding: 20px 30px;
  background: #17298b;
  border-radius: 30px 0px 30px 30px;
  font-size: 16px;
  font-family: Source Han Sans CN;
  font-weight: 400;
  color: #ffffff;
  margin-top: 10px;
  line-height: 24px;
  max-width: 860px;
}


.middle_key .middle_top .fr img {
  width: 40px;
}


.middle_key .middle_box {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
}

.middle_key .middle_box .fl {
  padding-left: 20px;
  margin-top: 10px;
}

.middle_key .middle_box .fl p {
  text-align: left;
  font-size: 16px;
  font-family: Source Han Sans CN;
  font-weight: 400;
  color: #999999;
}

.middle_key .middle_box .fl div {
  padding: 20px 30px;
  background: #f2f4fc;
  border-radius: 0px 40px 40px 40px;
  font-size: 16px;
  font-family: Source Han Sans CN;
  font-weight: 400;
  color: #333333;
  line-height: 24px;
  margin-top: 10px;
  max-width: 860px;
}


.middle_key .middle_box .fr img {
  width: 40px;
}

.middle_list {
  width: 100%;
  height: 80px;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 0 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  bottom: 0px;
  left: 0px;
}

.middle_list .fl {
  display: flex;
  align-items: center;
}

.middle_list .fl img {
  width: 14px;
}

.middle_list .fl input {
  padding-left: 20px;
  width: 80%;
  outline: none;
  background: none;
  border: none;
}

.middle_list .fr {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 48px;
  background: #29af3f;
  border-radius: 24px;
}

.middle_list .fr span {

  font-family: Source Han Sans CN;

  color: #ffffff;
  padding-right: 11px;
}

.middle_list .fr img {
  width: 14px;
}

@media (min-width: 1920px) {}

@media (max-width: 1919px) {}
</style>