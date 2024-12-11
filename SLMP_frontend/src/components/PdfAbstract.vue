<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchFileMeta } from '@/api/paperExtract'
import { type metaType } from '@/api/commonType'
const props = defineProps({ fileId: String })

const fileMetaList = ref<metaType[]>();
function fetchMeta(fileId: string) {
  fetchFileMeta(fileId).then((response: any) => {
    fileMetaList.value = response.data.data
  })
}

function showMeta(metas:Array<metaType>) {
  fileMetaList.value = metas
}

defineExpose({
  fetchMeta,
  showMeta
});

</script>
<template >
  <el-descriptions class="margin-top" :column="1" border>

    <el-descriptions-item v-for="(item, index) in fileMetaList" :key="index">
      <template #label>
        <div class="cell-item">

          {{ item.metaKey }}
        </div>
      </template>
      {{ item.metaValue }}
    </el-descriptions-item>
  </el-descriptions>
</template>

<style scoped></style>