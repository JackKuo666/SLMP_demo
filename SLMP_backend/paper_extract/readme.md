# paper meta extract

# 1.原理步骤

1.输入pdf地址

2.抽取文本结果 

3.抽取文本full text

4.调用chatgpt3.5抽取meta字段

5.输出meta字段

# 2.依赖
python3.8
```pycon
requirements.txt
```

运行：`python fast_api.py`

# 3.接口使用
```pycon
curl --location --request POST 'http://localhost:8877/paperExtract' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "1",
    "url": "http://localhost:9000/zjlabko/%2FpaperExtract/4e5109fc-dbe4-456d-91c2-6926edaad77e_01-2018-A%20metagenomics%20roadmap%20to%20the%20uncultured%20genome%20diversity%20in%20hypersaline%20soda%20lake%20sediments.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230727T025243Z&X-Amz-SignedHeaders=host&X-Amz-Expires=431999&X-Amz-Credential=kominioadmin%2F20230727%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ffccb77ce4728083fc0bc870a92435a77b3ea105f7b0e755e04acd9a161934de"
}'
```

```pycon
{
    "id": "1",
    "title": "A metagenomics roadmap to the uncultured genome diversity in hypersaline soda lake sediments",
    "journal": "Microbiome",
    "year": "2018",
    "author": [
        "Charlotte D. Vavourakis",
        "Adrian-Stefan Andrei",
        "Maliheh Mehrshad",
        "Rohit Ghai",
        "Dimitry Y. Sorokin",
        "Gerard Muyzer"
    ],
    "institution": [
        "Department of Freshwater and Marine Ecology, Institute for Biodiversity and Ecosystem Dynamics, Faculty of Science, University of Amsterdam"
    ],
    "email": [
        "G.Muijzer@uva.nl"
    ],
    "response_text": "{\n\"title_of_the_paper\": \"A metagenomics roadmap to the uncultured genome diversity in hypersaline soda lake sediments\",\n\"journal_of_the_paper\": \"Microbiome\",\n\"year_of_the_paper\": \"2018\",\n\"author_of_the_paper\": [\"Charlotte D. Vavourakis\", \"Adrian-Stefan Andrei\", \"Maliheh Mehrshad\", \"Rohit Ghai\", \"Dimitry Y. Sorokin\", \"Gerard Muyzer\"],\n\"the_institution_of_the_author_of_the_paper\": [\"Department of Freshwater and Marine Ecology, Institute for Biodiversity and Ecosystem Dynamics, Faculty of Science, University of Amsterdam\"],\n\"email\": [\"G.Muijzer@uva.nl\"]\n}"
}
```

如果出现：pdf没法下载，那么response_text: "No pdf", 其他字段为空 
如果出现：chatgpt接口问题，那么response_text: ”No response“ 
