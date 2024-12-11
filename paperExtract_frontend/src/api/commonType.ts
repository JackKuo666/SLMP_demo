export type Paper = {
    id: number
    title: string
    authors: string
    url:string
    abstract: string
    tags: Array<string>
    metas:Array<metaType>
}


export interface LinkItem {
    value: string
    link: string
}

export type PaperFileType = {
    id: string,
    name: string,
    isExtract: string,
    status: string,
    statusDesc: string,
    tag: string,
    tags: Array<string> | null,
    gmtModified: Date,
    selectBtnDesc: string,
    pdfUrl: string,
    isActive: boolean
}

export type metaType = {
    fileId:number,
    metaKey:string,
    metaValue:string
}

export type QaType = {
    question: string,
    answer: string
  }