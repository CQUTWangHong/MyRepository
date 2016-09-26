'''
Created on 2016-8-19

@author: Administrator
'''
import re
import os
line = '''<li><div class="dd_lm">[<a href=http://www.chinanews.com/china.shtml>国内</a>]</div> <div class="dd_bt">
<a href="http://www.chinanews.com/gn/2016/09-11/8000830.shtml">
柬埔寨首相洪森：推动区域互联互通 深化中国—东盟合作发展</a></div><div class="dd_time">9-11 14:38</div></li''';
pattern = re.compile('shtml>(.*?)</a>.*?'
                     +'class="dd_bt"><a href="(.*?)".*?'
                     +'>(.*?)</a>.*?'
                     +'"dd_time">(.*?)</div>.*?')
# line = re.sub("\n","",line)
# line = re.sub("    ","", line)
# searchObj = pattern.findall(line)   #findall返回一个列表，列表里存储元组
# # print(searchObj)
# for s in searchObj:
#     print(s)
text = r'''      <div class="left_zw" style="position:relative">  
<p>　　<a target='_blank' href='http://www.chinanews.com/'>中新社</a>南宁9月11日电 (陈燕)“南宁具有独特的区位优势，中国—东盟博览会是台商拓展大陆和东盟市场的重要平台，我们自然不能缺席。”台湾贸易中心副秘书长叶明水11日在南宁说。</p>

<p>　　第13届中国-东盟博览会9月11日至14日在南宁国际会展中心举行。连续5年组团参加展会的台湾贸易中心，今年再度在东盟博览会上设立台湾精品馆，展出61件获得“台湾精品奖”的台湾名优产品，这些2016年度全新评选的高科技台湾精品都是首次亮相广西南宁。</p>

<p>　　据介绍，今年以“智慧生活”为主题的台湾精品馆，30家知名台湾企业展出的61件顶尖产品，分别涵盖智能科技、文化创意、运动健身、居家生活等多个方面。台湾贸易中心还特别邀请厂商代表，现场解读台湾精品智能科技产品，为台湾精品发声。</p>

<p>　　叶明水表示，台湾贸易中心积极组团参加大陆各地重要展会和边境展，以及通过举办台湾名品展、拓销团等活动，助力台湾厂商进行市场拓销与布局，全方面协助业者开发大陆内需市场及边境贸易商机。<table border=0 cellspacing=0 cellpadding=0 align=left style="padding-right:10px;"><tr><td><div id=adhzh name=hzh>

<div style="position: relative; width: 300px;height: 250px;">

<!-- 1807：新闻通发页 大画 类型：固定广告位 尺寸：300x250 -->
<script type="text/javascript">//<![CDATA[
ac_as_id = 1807;
ac_format = 0;
ac_mode = 1;
ac_group_id = 1;
ac_server_base_url = "me.afp.chinanews.com/";
//]]></script>
<script type="text/javascript" src="http://i8.chinanews.com/gg/yichuanmei/k.js"></script>

<img width="30" height="17"  src="http://i8.chinanews.com/gg/160711/ad_4.png" style="position: absolute; right: 0px; bottom: 0px; z-index: 999; border: none; width: 30px; height: 17px;"></div>
</div>
<!--[4,175,19] published at 2016-08-12 09:36:20 from #10 by 郑振海--></td></tr></table></p>

<p>　　他还表示，台湾企业拥有傲人的创新研发技术及市场敏锐度，台湾精品厂商希望透过东盟博览会，带给当地的民众更多新奇科技与生活乐趣，同时也让台湾精品进一步拓展到广西及东盟等区域，达到多方经贸交流的目标。</p>

<p>　　记者在现场看到，今年台湾精品馆以高端互动、崭新造型展现台湾精品与创新，馆内更精心打造体验情境，让与会客商透过感官了解体验台湾产品时尚魅力。展示的多项得奖产品包括：使用手机APP控制就能轻松像花朵一样展开的变形电脑机壳、微邦科技的携带式简易雾化治疗器、长天科技的宝宝照护系统，以及台湾维顺的5秒折迭电动代步车等。另外还有多款智慧科技、运动乐活、环保生活的展示主题，展现台湾精品“创新价值”精神。</p>

<p>　　台湾精品馆展出的各种创意十足又紧贴生活的科技潮品吸引了许多中外客商驻足停留。来自缅甸的参展商Lin Pyae Htun告诉记者说，他对现场展出的微电脑电锅非常感兴趣，觉得这个智慧电饭锅在缅甸很有市场，希望有机会可以去台湾进一步了解。</p>

<p>　　“我们注意到大陆民众以及东南亚国家对科技产品需求越来越高，所以这次带来一些设计新颖的‘智慧生活’产品。”参展台商程宇杰说，这些产品如果可以通过广西进入东盟国家市场，将会有更好的前途。</p>

<p>　　泰国曼谷台商联谊会会长许淑珍表示，台湾的电子产品在泰国很受青睐。台商普遍看好广西作为面向东盟开放交流的前沿和窗口作用，希望借助东盟博览会，与前来参展的泰国企业相互交流，促进合作。</p>

<p>　　“台湾精品奖”是台湾产品研发创新的权威奖项，每年一届选拨，至今已经举办20多年。该奖项从早期致力于扭转台湾产品形象，到现阶段强调台湾产品的“创新价值”，已经成为台湾产品追求成长的标杆。</p>

<p>　　叶明水说，通过这几年参加中国—东盟博览会，收获了不少东南亚客商的关注。台湾贸易中心将会以台湾精品馆展现其带领台湾产业走向世界舞台的坚决信心，也为台湾精品厂商搭建双赢的商务合作平台。(完)<div id="function_code_page"></div>  

'''

pattern = re.compile(r'<div class="left_zw" style="position:relative">  '
                       r'(.*)<div id="function_code_page">',re.S)
text = pattern.findall(text)
text = text[0]
labels=re.compile(r'[/]*<.*?>',re.S)
text = re.sub(labels,'',text)#去掉各种标签
text = re.sub("\n","",text)
text = re.sub(r'　　','\n',text)#将缩进符替换成换行符
print(text)
print(len(text))
s = '[国务院/nt  侨办/j]nt  发表/v  新年/t  贺词/n '
ss = '今天/t  上午/t  ，/w  [中共中央/nt  政治局/n]nt  委员/n  李/nr  铁映/nr  与/c  [广播/vn  电影/n  电视/n  部/n]nt  部长/n  孙/nr  家正/nr  、/w  [国家/n  语委/j]nt  主任/n  许/nr  嘉璐/nr  等/u  ，/w  向/p  第一/m  批/q  获得/v  《/w  播音员/n  主持人/n  资格/n  证书/n  》/w  的/u  中央/n  三/m  台/n  代表/n  颁证/v  。/w  '
# pattern1 = re.compile('\[(.*?)\]')#查找组合命名实体
# pattern2 = re.compile("/(\S+)")#找到所有词性
# pattern3 = re.compile("/n(\S+)")#找到所有命名实体
# pattern4 = re.compile('\[(.*?)\]n(\S+)')
# result = pattern1.finditer(ss)
# length = []
# for m in result:
#     length.append(len(m.group(1).split('  ')))
# print(length)
# result4 = pattern4.finditer(ss)
# count = 0
# for m4 in result4:
#     word = m4.group()[-2:]
#     string = ''
#     if length[count]==2:
#         string = '/B-'+word+' /E-'+word
#     elif length[count]>2:
#         string ='/B-'+word
#         for i in range(length[count]-2):
#             string = string+' /M-'+word
#         string = string+' /E-'+word
#     else:
#         print('组合命名实体长度有误')
#     ss = ss.replace(m4.group(), string)
#     count += 1
# result2 = pattern2.finditer(ss)
# for m2 in result2:
#     print(m2.group())
    
# print(ss)
#     if 'B-'+l[0][-2:] in 
#     for k in l:
#     if 'E-'+l[len(l)-1][-2:] in
    
# if '[' or ']' in ss:
# ss = re.sub(r'\[(.*?)\]','/',ss)
# print('ss',ss)
# result2 = pattern2.finditer(ss)
# for m2 in result2:
#     print(m2.group())

# result = pattern3.finditer(ss)
# for m in result:
#     print(m.group())





   