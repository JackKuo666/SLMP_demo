import request from '@/router/axios'
import type { Paper } from './commonType'

export function addOnline(paper:Paper) {
    return request({
        url:'/kodata/userextractfile/addOnline',
        method:'post',
        data:paper
    })
}

export function queryEsByKey(keyword:string) {
  return request({
    url:"/pees/complete",
    method:'get',
    params:{
      
      keyword:keyword
    }
  })
}


export function pageEs(current:number,size:number,keyword:string) {
  return request({
    url:"/pees/page",
    method:'get',
    params:{
      current:current,
      size:size,
      keyword:keyword
    }
  })
}
