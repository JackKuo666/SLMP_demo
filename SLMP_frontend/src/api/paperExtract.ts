import request from '@/router/axios'

export function pageUserFile(query: {}) {
    return request({
        url:'/kodata/userextractfile/page',
        method:'get',
        params:query
    })
}

export function handlePaperFile(id:string) {
    return request({
        url:'/kodata/userextractfile/extract',
        method:'get',
        params:{"id":id}
    })
}

export function fetchFileMeta(id:string) {
    return request({
        url:'/kodata/extractfilemeta/listFileMeta',
        method:'get',
        params:{"fileId":id}
    })
}

export function getFileUrl(fileId:string) {
    return request({
        url:'/kodata/userextractfile/fileUrl',
        method:'get',
        params:{"fileId":fileId}
    })
}

export function sendQuestion(query:string, fileId:string, history:string) {
    return request({
        url:'/kodata/userextractfile/question',
        method:'post',
        data:{"fileId":fileId,"q":query,'history':history}
    })
}

export function checkKbStatus(fileId:string) {
    return request({
        url:'/kodata/userextractfile/checkKbStatus',
        method:'get',
        params:{"fileId":fileId}
    })
}