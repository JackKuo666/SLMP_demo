<template>
    <div class="zhjxMain">
        <div class="content">
            <!-- 展示容器 -->
            <div class="left-box" :ref="refs.wrapper" @wheel.prevent="scaleWheel($event)">
                <div class="box" :ref="refs.box" @mousedown="dragstart($event)">
                    <vue-pdf-embed :source="scaleData.source" :style="scaleFun" class="vue-pdf-embed"
                        :page="scaleData.pageNum" />
                </div>


                <div class="page-tool">
                    <div class="page-tool-item" @click="lastPage">上一页</div>
                    <div class="page-tool-item" @click="nextPage">下一页</div>
                    <div class="page-tool-item">{{ scaleData.pageNum }}/{{ scaleData.numPages }}</div>
                    <div class="page-tool-item" @click="rollBtn('enlarge')">放大</div>
                    <div class="page-tool-item">{{ Math.trunc(scaleData.scale * 100) }} %</div>
                    <div class="page-tool-item" @click="rollBtn('zoomin')">缩小</div>
                </div>
            </div>

        </div>
    </div>
</template>
  
<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted } from 'vue';
import VuePdfEmbed from 'vue-pdf-embed';
import { createLoadingTask } from "vue3-pdfjs";


const props = defineProps({
    pdfUrl: {
        type: String,
        required: true
    }
})


const scaleData = reactive({
    scale: 1, // 缩放比例
    scaleNum: 0.1, // 滚轮缩放比例
    scaleMax: 100, // 最大缩放比例
    scaleMin: 0.1, // 最小缩放比例
    scaleBtn: 0.4, // 缩放按钮缩放比例
    rotate: 0, // 旋转角度
    source: props.pdfUrl,
    pageNum: 1,

    numPages: 0, // 总页数
});
function lastPage() {
    if (scaleData.pageNum > 1) {
        scaleData.pageNum -= 1;
    }
}
function nextPage() {
    if (scaleData.pageNum < scaleData.numPages) {
        scaleData.pageNum += 1;
    }
}


// 实现pdf缩放
const scaleFun = computed(() => {
    return `transform:scale(${scaleData.scale});transition: all 0.3s;`;
});
const refs = {
    wrapper: ref<HTMLElement>(), // pdf外层容器
    box: ref<HTMLElement>(), // pdf容器，用于拖拽
};
const dragData = reactive({
    x: 0, // 拖拽初始化时的x坐标
    y: 0, // 拖拽初始化时的y坐标
    left: 0, // 拖拽结束时的x偏移量
    top: 0, // 拖拽结束时的y偏移量
    firstX: 0, // 初始x坐标
    firstY: 0, // 初始y坐标
});


watch(
    () => props.pdfUrl,
    (v) => {
        // 重置pdf大小和位置
        scaleData.scale = 1;
        scaleData.rotate = 0;
        const box = refs.box.value as HTMLElement;
        box.style.left = '50%';
        box.style.top = '50%';
        boxTransform();
    },
);

onMounted(() => {
    loadPdf(props.pdfUrl)

});
defineExpose({
    loadPdf,
});

function loadPdf(pdfSrc: string) {
    console.log("load pdf")
    scaleData.source = pdfSrc
    scaleData.pageNum = 1
    const loadingTask = createLoadingTask(scaleData.source);
    loadingTask.promise.then((pdf: { numPages: number }) => {
        scaleData.numPages = pdf.numPages;
    });
}

// box 容器也要跟着变化
const boxTransform = () => {
    const box = refs.box.value as HTMLElement;
    box.style.transform = `translate(-50%, -50%) rotate(${scaleData.rotate}deg) scale(${scaleData.scale})`;
};


// 鼠标滚轮缩放
function scaleWheel(e: any) {
    let dy = -e.deltaY || e.wheelDeltaY;
    if (dy < 0) {
        scaleData.scale -= scaleData.scaleNum;
    } else {
        // console.log('放大');
        scaleData.scale += scaleData.scaleNum;
    }
    // 边界判断
    if (scaleData.scale >= scaleData.scaleMax) {
        scaleData.scale = scaleData.scaleMax;
        return;
    }
    if (scaleData.scale <= scaleData.scaleMin) {
        scaleData.scale = scaleData.scaleMin;
        return;
    }
    boxTransform();
    return false;
}

// 点击放大缩小
const rollBtn = (action: 'enlarge' | 'zoomin') => {
    if (action === 'enlarge') {
        scaleData.scale += scaleData.scaleBtn;
    } else {
        scaleData.scale -= scaleData.scaleBtn;
    }
    // 边界判断
    if (scaleData.scale >= scaleData.scaleMax) {
        scaleData.scale = scaleData.scaleMax;
        return;
    }
    if (scaleData.scale <= scaleData.scaleMin) {
        scaleData.scale = scaleData.scaleMin;
        return;
    }
    boxTransform();
};

// 拖拽（box容器拖拽）
function dragstart(e: MouseEvent) {
    const box = refs.box.value as HTMLElement;
    box.style.transition = 'none';
    e.preventDefault(); // 阻止默认事件

    dragData.x = e.pageX - box.offsetLeft;
    dragData.y = e.pageY - box.offsetTop;

    // 添加鼠标移动事件
    document.addEventListener('mousemove', move);
    function move(event: any) {
        // 计算元素的位置
        dragData.left = event.pageX - dragData.x;
        dragData.top = event.pageY - dragData.y;
        // 边界判断可以在这里添加 ↓

        // 设置元素的位置
        box.style.left = dragData.left + 'px';
        box.style.top = dragData.top + 'px';
    }
    // 添加鼠标抬起事件，鼠标抬起，将事件移除
    document.addEventListener('mouseup', function () {
        document.removeEventListener('mousemove', move);
    });
    // 鼠标离开父级元素，把事件移除
    document.addEventListener('mouseout', function () {
        document.removeEventListener('mousemove', move);
    });
}
</script>
  
<style scoped lang="scss">
.zhjxMain {
    width: 100%;
    height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;

    overflow: hidden;

    .content {
        width: 100%;
        height: 100%;
        margin: 0 auto;

        display: flex;
        overflow: hidden;

        .left-box {
            width: 100%;
            height: 100%;
            background-color: #26262623;
            position: relative;
            overflow: hidden;

            .box {
                width: 50%;
                height: 100%;
                object-fit: contain;
                user-select: none;
                /* 不可选中,为了拖拽时不让文字高亮 */
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                display: flex;
                align-items: center;
                justify-content: center;

                .vue-pdf-embed {
                    width: 100%;
                    cursor: pointer;
                }
            }
        }
    }
}

.page-tool {
    position: absolute;
    bottom: 5px;
    padding-left: 15px;
    padding-right: 15px;
    display: flex;
    align-items: center;
    background: rgb(66, 66, 66);
    color: white;
    border-radius: 19px;
    z-index: 100;
    cursor: pointer;
    margin-left: 50%;
    transform: translateX(-50%);
}

.page-tool-item {
    padding: 8px 15px;
    padding-left: 10px;
    cursor: pointer;
}
</style>
  