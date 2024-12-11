import requests
import fitz
import os
import csv
from 通用_section转字段_gpt35 import prompt_function, chatgpt_extract


def download_pdf(url, pdf_folder, pdf_id=1):
    try:
        response = requests.get(url)
        pdf_dir = pdf_folder + '/{0}_download.pdf'.format(pdf_id)
        with open(pdf_dir, 'wb') as f:
            f.write(response.content)
        print("write in:"+pdf_dir)
        return pdf_dir
    except:
        print("error get pdf:" + str(pdf_dir))
        return None


def get_full_text(doc):
    page_count = doc.page_count
    res = {}
    for page in range(page_count):
        text = doc.load_page(page).get_text("text")
        res[page] = text

    return res


def extract_pdf(pdf_dir):
    result = {'file_name': "", 'first_page': "",
              "meta_title": "",
              "meta_author": "",
              "meta_subject": "",
              "meta_keywords": "",
              "meta_creator": "",
              "meta_creationDate": ""
              }
    try:
        doc = fitz.open(pdf_dir)
    except:
        print("can not read pdf")
        return result, None
    # 1.获取meta信息
    metadata = doc.metadata
    print(doc.metadata)
    result["file_name"] = dir
    result["meta_title"] = metadata["title"]
    result["meta_author"] = metadata["author"]
    result["meta_subject"] = metadata["subject"]
    result["meta_keywords"] = metadata["keywords"]
    result["meta_creator"] = metadata["creator"]
    result["meta_creationDate"] = metadata["creationDate"]

    #  2.获取第一页文本
    result["first_page"] = doc.load_page(0).get_text("text") if doc.page_count > 0 else ""
    # a.天文类文章需要两页
    if "Research in Astronomy and Astrophysics" in result["first_page"]:
        result["first_page"] += doc.load_page(1).get_text("text") if doc.page_count > 0 else ""
    # b.制药类文章如果有这个标志，会两页
    elif "Just Accepted" in result["first_page"]:
        result["first_page"] += doc.load_page(1).get_text("text") if doc.page_count > 0 else ""
    # c.材料领域出现这个标注，需要两页
    elif "Published by the American Institute of Physics" in result["first_page"]:
        result["first_page"] += doc.load_page(1).get_text("text") if doc.page_count > 0 else ""
    # d.材料领域出现这个标注，需要两页
    elif "Published by the AIP Publishing" in result["first_page"]:
        result["first_page"] += doc.load_page(1).get_text("text") if doc.page_count > 0 else ""
    # e.材料领域出现这个标注，需要两页
    elif "Articles you may be interested in" in result["first_page"]:
        result["first_page"] += doc.load_page(1).get_text("text") if doc.page_count > 0 else ""


    # 3.获取full_text文本
    full_text = get_full_text(doc)
    # print(result["full_text"])

    # for i in result:
    #     print(i, "==xxxx==",result[i])

    return result, full_text


def write_middle_file(pdf_folder, full_text, extract_result, pdf_id):
    fieldnames = ['file_name', 'first_page', 'meta_title', 'meta_author', 'meta_subject', 'meta_keywords',
                  'meta_creator', 'meta_creationDate']
    with open(pdf_folder + '/{0}_抽取文本结果.csv'.format(pdf_id), mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 判断表格内容是否为空，如果为空就添加表头
        if not os.path.getsize(pdf_folder + '/{0}_抽取文本结果.csv'.format(pdf_id)):
            writer.writeheader()  # 写入表头
        with open(pdf_folder + "/{0}_full_text.txt".format(pdf_id), mode='w', encoding='utf-8') as fout:
            fout.write(str(full_text))
        writer.writerow(extract_result)
    print("抽取文本结果 write in: ", pdf_folder + '/{0}_抽取文本结果.csv'.format(pdf_id))
    print("抽取文本full text write in: ", pdf_folder + "/{0}_full_text.txt".format(pdf_id))


def write_model_extract_file(pdf_folder, pdf_id, extract_result):
    fieldnames = ['id', 'title',
                  'journal', 'year', 'author',
                  'institution', 'email', 'response_text']
    with open(pdf_folder + '/{0}_抽取字段结果.csv'.format(pdf_id), mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 判断表格内容是否为空，如果为空就添加表头
        if not os.path.getsize(pdf_folder + '/{0}_抽取字段结果.csv'.format(pdf_id)):
            writer.writeheader()  # 写入表头
        writer.writerow(extract_result)
    print("extract data write in: ", pdf_folder + '/{0}_抽取字段结果.csv'.format(pdf_id))


def meta_extract(url, pdf_id):
    pdf_folder = './tmp_pdf'
    pdf_dir = download_pdf(url, pdf_folder, pdf_id)
    extract_result = {'id': pdf_id,
     'title': "", 'journal': "", 'year': "",
     'author': [], 'institution': [], 'email': [],
     "response_text": "No pdf"}
    if pdf_dir:
        pdf_result, full_text = extract_pdf(pdf_dir)
        if full_text:
            write_middle_file(pdf_folder, full_text, pdf_result, pdf_id)
            response = prompt_function(pdf_result['first_page'])
            if response:
                print(response.choices[0].message.content)
                # 这里chatgpt输出结果可能存在不稳定的情况，需要做跟标准输出做对齐
                extract_result = chatgpt_extract(response.choices[0].message.content)
            else:
                extract_result["response_text"] = "No response"
            extract_result['id'] = pdf_id
            write_model_extract_file(pdf_folder, pdf_id, extract_result)

    return extract_result


if __name__ == "__main__":
    url = f'http://localhost:9000/zjlabko/%2FpaperExtract/4e5109fc-dbe4-456d-91c2-6926edaad77e_01-2018-A%20metagenomics%20roadmap%20to%20the%20uncultured%20genome%20diversity%20in%20hypersaline%20soda%20lake%20sediments.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230727T025243Z&X-Amz-SignedHeaders=host&X-Amz-Expires=431999&X-Amz-Credential=kominioadmin%2F20230727%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ffccb77ce4728083fc0bc870a92435a77b3ea105f7b0e755e04acd9a161934de'

    pdf_id = 1
    extract_result = meta_extract(url, pdf_id)
    print(extract_result)