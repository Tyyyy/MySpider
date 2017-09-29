import requests
import re
import os
import sys
import json

# B站API详情 https://github.com/Vespa314/bilibili-api/blob/master/api.md

# 视频AV号列表
aid_list = []

# 评论用户及其信息
info_list = []

# 获取指定UP的所有视频的AV号 mid:用户编号 size:单次拉取数目 page:页数
def getAllAVList(mid, size, page):
    # 获取UP主视频列表
    for n in range(1,page+1):
        url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
            str(mid) + "&pagesize=" + str(size) + "&page=" + str(n)
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        for item in json_text["data"]["vlist"]:
            aid_list.append(item["aid"])
    print(aid_list)

# 获取一个AV号视频下所有评论
def getAllCommentList(item):
    url = "http://api.bilibili.cn/feedback?aid=" + str(item)
    r = requests.get(url)
    numtext = r.text
    json_text = json.loads(numtext)
    commentsNum = json_text["results"]
    page = commentsNum // 20 + 1
    for n in range(1,page):
        url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn="+str(n)+"&type=1&oid="+str(item)+"&sort=1&nohot=1"
        req = requests.get(url)
        text = req.text
        json_text_list = json.loads(text)
        for i in json_text_list["data"]["replies"]:
            info_list.append([i["member"]["uname"],i["content"]["message"]])
    # print(info_list)

# 保存评论文件为txt
def saveTxt(filename,filecontent):
    filename = str(filename) + ".txt"
    print("文件"+str(filename)+"写入中")
    for content in filecontent:
        if content[0] == '':
            with open(filename, "a", encoding='utf-8') as txt:
                if content[0] == '':
                    txt.write(content[0] +' '+content[1].replace('\n','') + '\n\n')
    

if __name__ == "__main__":
    # 爬取逆风笑 只爬取第一页的第一个
    getAllAVList(2019740,20,30)
    for item in aid_list:
        info_list.clear()
        getAllCommentList(item)
        saveTxt(item,info_list)

