# import os module & the OpenAI Python library for calling the OpenAI API
import os
import openai
import json
import pandas as pd
from tqdm import tqdm
import time

# Load config values
with open(r'D:\code\4.宏基因组论文抽取\config.json') as config_file:
    config_details = json.load(config_file)

chatgpt_model_name = config_details['CHATGPT_MODEL']

openai.api_type = "azure"

openai.api_key = config_details["OPENAI_API_KEY"]
openai.api_base = config_details['OPENAI_API_BASE']

openai.api_version = config_details['OPENAI_API_VERSION']

a="""
0.当前最好版本：
    【无email、机构和作者关联】：    
         could you please help me extract the information of 'title_of_the_paper'/'journal_of_the_paper'/'year_of_the_paper'/'author_of_the_paper'/'the_institution_of_the_author_of_the_paper'/'email' from the previous content in a json format?
         If any of this information was not available in the paper, please replaced it with the string `""`, If the property contains multiple entities, please use a list to contain.


1.空字符形式：
    1.1.原始版本：
        If there do not exist one of these information, please tell me 'No specific information about yield'
    1.2.修改版本            
        If there do not exist one of these information, please tell me ''
    1.3.修改版本
        If any of the information is missing, the value in the JSON will be ""
    1.3.修改版本
        If any of this information was not available in the paper, please replaced it with the string `""`
    
2.多个实体使用list:
    If the field contains multiple entities, please use list to contain.

3.【email、机构和作者关联】
    效果不好：
         could you please help me extract the information of 'title_of_the_paper'/'journal_of_the_paper'/'year_of_the_paper'/'authors_of_the_paper', as well as the 'institution' and 'email address' of the corresponding 'authors_of_the_paper' from the previous content in a json format?
         If any of this information was not available in the paper, please replaced it with the string `""`. please extract all of the information, do not use `...`.

"""


def prompt_function(content):
    try:

        response = openai.ChatCompletion.create(
            engine=chatgpt_model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": """
                
                The following is part of a paper:

                """ + content +
                 """

                 could you please help me extract the information of 'title_of_the_paper'/'journal_of_the_paper'/'year_of_the_paper'/'author_of_the_paper'/'the_institution_of_the_author_of_the_paper'/'email' from the previous content in a json format?
                 If any of this information was not available in the paper, please replaced it with the string `""`, If the property contains multiple entities, please use a list to contain.

             
                 """}
            ]
        )

        return response

    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")

    except openai.error.AuthenticationError as e:
        # Handle Authentication error here, e.g. invalid API key
        print(f"OpenAI API returned an Authentication Error: {e}")

    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")

    except openai.error.InvalidRequestError as e:
        # Handle connection error here
        print(f"Invalid Request Error: {e}")

    except openai.error.RateLimitError as e:
        # Handle rate limit error
        print(f"OpenAI API request exceeded rate limit: {e}")

    except openai.error.ServiceUnavailableError as e:
        # Handle Service Unavailable error
        print(f"Service Unavailable: {e}")

    except openai.error.Timeout as e:
        # Handle request timeout
        print(f"Request timed out: {e}")

    except:
        # Handles all other exceptions
        print("An exception has occured.")

    return None


def list2str(text):
    text = str(text) if type(text) is not str else text
    return text


def str2list(text):
    if type(text) is str:
        return text.split(',')
    elif type(text) is dict:
        return list(text.values())
    return text


def str2list_institution(text):
    if type(text) is str:
        return [text]
    elif type(text) is dict:
        return list(text.values())
    return text


def chatgpt_extract(result_json):
    extract_result = {'id': "",
                      'title': "", 'journal': "", 'year': "",
                      'author': "", 'institution': "", 'email': "",
                      "response_text": result_json}

    import json
    # 1.有些结果可能外部包含了一层list、可能不是纯dict,需要做提取
    import re
    result_pat = re.search(r'(\{(.|\n)*\})', result_json)
    if result_pat:
        result_json = str(result_pat.group())
    # print(result_json)
    # result_json = json.loads(result_json)
    try:
        result_json = json.loads(result_json)
    except:
        print("输出文本不是格式化的json,无法提取：", result_json)
        return extract_result

    # 2.有些结果名字可能和设定的有些出入，需要做字段名称对齐
    # 3.有些字段的内容可能是list,转成文本
    for key in result_json.keys():
        if "title" in key:
            extract_result["title"] = list2str(result_json[key])
        elif "journal" in key:
            extract_result["journal"] = list2str(result_json[key])
        elif "year" in key:
            extract_result["year"] = list2str(result_json[key])
        elif "author" in key and "institution" not in key:
            extract_result["author"] = str2list(result_json[key])
        elif "institution" in key:
            extract_result["institution"] = str2list_institution(result_json[key])
        elif "mail" in key:
            extract_result["email"] = str2list(result_json[key])
        else:
            print("result can't found in filed name: ", key)

    return extract_result


if __name__ == "__main__":
    response = prompt_function("""
    RESEARCH
Open Access
An integrated gene catalog and over
10,000 metagenome-assembled genomes
from the gastrointestinal microbiome of
ruminants
Fei Xie1†, Wei Jin1†, Huazhe Si2†, Yuan Yuan3†, Ye Tao4, Junhua Liu1, Xiaoxu Wang5, Chengjian Yang6,
Qiushuang Li7, Xiaoting Yan3, Limei Lin1, Qian Jiang1, Lei Zhang1, Changzheng Guo1, Chris Greening8,
Rasmus Heller9, Le Luo Guan10, Phillip B. Pope11, Zhiliang Tan7, Weiyun Zhu1, Min Wang7*, Qiang Qiu3*,
Zhipeng Li2,5* and Shengyong Mao1*
Abstract
Background: Gastrointestinal tract (GIT) microbiomes in ruminants play major roles in host health and thus animal
production. However, we lack an integrated understanding of microbial community structure and function as prior
studies are predominantly biased towards the rumen. In this study, we used shotgun metagenomics to profile the
microbiota of 370 samples that represent 10 GIT regions of seven ruminant species.
© The Author(s). 2021, corrected publication 2022. Open Access This article is licensed under a Creative Commons Attribution 4.0
International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if
changes were made. The images or other third party material in this article are included in the article's Creative Commons
licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons
licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.
The Creative Commons Public Domain Dedication waiver (http://creativecommons.org/publicdomain/zero/1.0/) applies to the
data made available in this article, unless otherwise stated in a credit line to the data.
* Correspondence: maoshengyong@njau.edu.cn; lizhipeng01@caas.cn;
qiuqiang@lzu.edu.cn; mwang@isa.ac.cn
†Fei Xie, Wei Jin, Huazhe Si and Yuan Yuan contributed equally to this work.
1Laboratory of Gastrointestinal Microbiology, College of Animal Science and
Technology, Nanjing Agricultural University, Nanjing, China
2College of Animal Science and Technology, Jilin Agricultural University,
Changchun, China
3School of Ecology and Environment, Northwestern Polytechnical University,
Xi’an, China
7CAS Key Laboratory for Agro-Ecological Processes in Subtropical Region,
Institute of Subtropical Agriculture, Chinese Academy of Sciences, Changsha,
China
Full list of author information is available at the end of the article
Xie et al. Microbiome           (2021) 9:137 
https://doi.org/10.1186/s40168-021-01078-x
    """)
    print(response)
    if response:
        print("response text:", response.choices[0].message.content)
    extract_result = chatgpt_extract(response.choices[0].message.content)
    print("extract_result", json.dumps(extract_result, indent=4))


    # pdf_folder = '3.天文/天文已标注文献'
    #
    # import csv
    #
    # fieldnames = ['file_name', 'title_of_the_paper',
    #               'journal_of_the_paper', 'year_of_the_paper', 'author_of_the_paper',
    #               'the_institution_of_the_author_of_the_paper', 'email', 'response_text']
    # with open(pdf_folder+'/抽取字段结果.csv', mode='w', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     # 判断表格内容是否为空，如果为空就添加表头
    #     if not os.path.getsize(pdf_folder+'/抽取字段结果.csv'):
    #         writer.writeheader()  # 写入表头
    #
    #     content = pd.read_csv(pdf_folder+'/抽取文本结果.csv')
    #     section_content_file_name = content['file_name'].values.tolist()
    #     section_content_first_page = content['first_page'].values.tolist()
    #
    #     for i in tqdm(range(len(section_content_first_page))):
    #         response = prompt_function(
    #             section_content_first_page[i])
    #         if response:
    #             print(section_content_file_name[i])
    #             print(response.choices[0].message.content)
    #             # 这里chatgpt输出结果可能存在不稳定的情况，需要做跟标准输出做对齐
    #             extract_result = chatgpt_extract(response.choices[0].message.content)
    #         else:
    #             extract_result = chatgpt_extract("No response")
    #         extract_result['file_name'] = section_content_file_name[i]
    #         time.sleep(10)
    #
    #         writer.writerow(extract_result)
    #
