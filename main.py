#coding:utf-8
#author:itacajsj@outlook.com
import urllib2,cookielib,re,urllib
from bs4 import BeautifulSoup
class szb():
    def __init__(self,user,pwd):
        import os
        #思修为12
        #近代史13
        #毛概  14
        #马原  15
        self.user=user
        self.pwd=pwd
        self.location=os.path.join(os.getcwd(),'data')
        self.starturl=r'http://szbks.njfu.edu.cn/index1.asp'
        self.loginurl=r'http://szbks.njfu.edu.cn/checkusr.asp?action=user'
        # button=+%B5%C7+%C2%BC+
        self.data=urllib.urlencode({"username":self.user,"pwd":self.pwd})+r"&button=+%B5%C7+%C2%BC+"
        self.makeopener()
        self.login()
    def makeopener(self):
        cookies=urllib2.HTTPCookieProcessor()
        opener=urllib2.build_opener(cookies)
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'),
                           ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                           ('Accept-Encoding','deflate'),
                           ('Connection','keep-alive'),
                           ('Host','szbks.njfu.edu.cn')
                           ]
        self.opener=opener
    def login(self):
        self.opener.open(self.starturl)
        self.opener.open(self.loginurl,self.data)
        self.opener.open('http://szbks.njfu.edu.cn/b2bsoft2.asp')
        # dats=self.opener.open('http://szbks.njfu.edu.cn/cx_paper.asp?kcid=15').read()
        # f=open('htm.txt','w')
        # f.write(dats.decode('gb2312').encode('utf-8'))
        # f.close()
    def get_mayuan(self):
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_paper.asp?kcid=15').read()
        htm=htm.decode('gb2312').encode('utf-8')
        pattern='href="(.+?)".+?>WORD</a>'
        urls=re.findall(pattern,htm)
        url=[]
        for i in urls:
            url.append('http://szbks.njfu.edu.cn/'+i)
        return url
    def get_maogai(self):
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_paper.asp?kcid=14').read()
        htm=htm.decode('gb2312').encode('utf-8')
        pattern='href="(.+?)".+?>WORD</a>'
        urls=re.findall(pattern,htm)
        url=[]
        for i in urls:
            url.append('http://szbks.njfu.edu.cn/'+i)
        return url
    def get_sixiu(self):
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_paper.asp?kcid=12').read()
        htm=htm.decode('gb2312').encode('utf-8')
        pattern='href="(.+?)".+?>WORD</a>'
        urls=re.findall(pattern,htm)
        url=[]
        for i in urls:
            url.append('http://szbks.njfu.edu.cn/'+i)
        return url
    def get_jindaishi(self):
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_paper.asp?kcid=13').read()
        htm=htm.decode('gb2312').encode('utf-8')
        pattern='href="(.+?)".+?>WORD</a>'
        urls=re.findall(pattern,htm)
        url=[]
        for i in urls:
            url.append('http://szbks.njfu.edu.cn/'+i)
        return url
    def creatfile(self,path,name):
        '''创建不重复文件'''
        import os
        if os.path.isdir(path) is False:
            os.mkdir(path)
        k=1
        name2=name+str(k)+'.doc'
        paths=os.path.join(path,name2)
        while os.path.exists(paths):
            k=k+1
            name2=name+str(k)+'.doc'
            paths=os.path.join(path,name2)
        return paths
    def get_word_to_file(self):
        url=[]
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_subject.asp').read().decode('gb2312').encode('utf-8')
        if re.search('马克思主义基本原理',htm):
            url=url+self.get_mayuan()
        if re.search('思想道德修养与法律基础',htm):
            url=url+self.get_sixiu()
        if re.search('中国近代史纲要',htm):
            url=url+self.get_jindaishi()
        if re.search('毛泽东思想和中国特色社会主义理论',htm):
            url=url+self.get_maogai()
        for it in url:
            f=open(self.creatfile(self.location,'TiKu'),'w')
            data=self.opener.open(it).read().decode('gb2312').encode('utf-8')
            f.write(data)
            f.close()
    def get_word_to_list(self):
        url=[]
        list=[]
        htm=self.opener.open('http://szbks.njfu.edu.cn/cx_subject.asp').read().decode('gb2312').encode('utf-8')
        if re.search('马克思主义基本原理',htm):
            url=url+self.get_mayuan()
        if re.search('思想道德修养与法律基础',htm):
            url=url+self.get_sixiu()
        if re.search('中国近代史纲要',htm):
            url=url+self.get_jindaishi()
        if re.search('毛泽东思想和中国特色社会主义理论',htm):
            url=url+self.get_maogai()
        for it in url:
            data=self.opener.open(it).read().decode('gb2312').encode('utf-8')
            list.append(data)
        return list
class tiqu():
    def __init__(self,data):
        self.data=data
        self.name=BeautifulSoup(self.data).title.text.split('|')[1].strip()
        self.dan=[]
        self.duo=[]
        self.pan=[]
        self.formats(self.get_questions())
        print self.name
    def get_questions(self):
        soup=BeautifulSoup(self.data)
        lb=''
        if re.search('毛泽东思想和中国特色社会主义理论体系',soup.title.prettify().encode('utf-8')) is not None:
            lb='mg'
        elif re.search('马克思主义基本原理',soup.title.prettify().encode('utf-8'))is not None:
            lb='my'
        elif re.search('思想道德修养与法律基础',soup.title.prettify().encode('utf-8'))is not None:
            lb='sx'
        elif re.search('近现代史',soup.title.prettify().encode('utf-8'))is not None:
            lb='jds'
        tables=soup.find_all('table')
        tag=0
        #tag=1为单选，2为多选，3为判断
        degree=0
        #degree=1为简单 2 为中等，3为较难，4为最难
        questions=[]
        #题目集
        for table in tables:
            trs=table.find_all('tr')
            print trs
            for tr in trs:
                print tr
                if tr.find_all('td')[1].find('b').contents[0]==u'单选题':
                    tag=1
                elif tr.find_all('td')[1].find('b').contents[0]==u'多选题':
                    tag=2
                elif tr.find_all('td')[1].find('b').contents[0]==u'判断题':
                    tag=3
                else:
                    tds=tr.find_all('td')
                    for a in tds:
                        text=a.text
                        texts=text.split('\n')
                        question=[]
                        question.append(tag)
                        for i in texts:
                            i=i.strip()
                            if i=='':
                                continue
                            if re.search(u'您的答案',i):
                                break
                            if i.isdigit():
                                print i
                                continue
                            if re.findall(u'\（难度：(.+?)\）',i):
                                question.append(re.findall(u'\（难度：(.+?)\）',i)[0].strip())
                                if len(i.split(u'――'))==2 and i.split(u'――')[1].strip():
                                    question.append(i.split(u'――')[1].strip())
                                elif len(i.split(u'――'))>2:
                                    print 'Error------------'
                                    print i
                                    print'--------------'
                                continue
                            question.append(i)
                        if len(question)>1:
                            questions.append(question)
        return questions
    def formats(self,c):
        all=[]
        for i in c:
            dic={}
            tag=i[0]
            dic['nandu']=i[1]
            dic['title']=i[2]
            if tag==2 or tag==1:
                #单选或者多选
                danindex=len(i)
                for j in range(3,len(i)):
                    if re.search(u'标准答案',i[j]):
                        danindex=j
                        break
                    print i[j]
                    name=i[j].split('.')[0]
                    valu=i[j].split('.')[1]
                    dic[name]=valu
                answer=''
                for j in range(danindex,len(i)):
                    str=i[j].replace(u'标准答案：','').strip()
                    answer=answer+str.split('.')[0]+','
                answer=answer.strip(',')
                dic['answer']=answer
            elif tag==3:
                dic['answer']=i[3].replace(u'标准答案：','').strip()
            if tag==1:
                self.dan.append(dic)
            elif tag==2:
                self.duo.append(dic)
            elif tag==3:
                self.pan.append(dic)
class sqlites():
    def __init__(self,name):
        import sqlite3
        curs=sqlite3.connect(name+'.db')
        cmd=curs.cursor()
        cmd.execute("create table if not EXISTS danxuan(id integer PRIMARY KEY AUTOINCREMENT ,nandu char,title char,A char,B char,C char,D char, answer char)")
        cmd.execute("create table if not EXISTS duoxuan(id integer PRIMARY KEY AUTOINCREMENT  ,nandu char,title char,A char,B char,C char,D char, E char , F char,G char,H char,I char,answer char)")
        cmd.execute("create table if not EXISTS panduan(id integer PRIMARY KEY AUTOINCREMENT  ,nandu char,title char,answer int)")
        self.cmd=cmd
        self.curs=curs
    def Idanxuan(self,dic):
        if not self.check(dic,'danxuan'):
            cmdstr="INSERT INTO danxuan ("
            value="("
            for key in dic.keys():
                cmdstr=cmdstr+key+','
                value=value+"'"+dic[key]+"',"
            cmdstr=cmdstr.strip(',')+') values'+value.strip(',')+');'
            self.cmd.execute(cmdstr)
            self.curs.commit()
        else:
            print '重复'+dic['title']
            # cmd.execute(cmdstr)
    def Iduoxuan(self,dic):
        if not self.check(dic,'danxuan'):
            cmdstr="INSERT INTO duoxuan ("
            value="("
            for key in dic.keys():
                cmdstr=cmdstr+key+','
                value=value+"'"+dic[key]+"',"
            cmdstr=cmdstr.strip(',')+') values'+value.strip(',')+');'
            self.cmd.execute(cmdstr)
            self.curs.commit()
        else:
            print '重复'+dic['title']
    def Ipanduan(self,dic):
        if not self.check(dic,'danxuan'):
            cmdstr="INSERT INTO panduan ("
            value="("
            for key in dic.keys():
                cmdstr=cmdstr+key+','
                value=value+"'"+dic[key]+"',"
            cmdstr=cmdstr.strip(',')+') values'+value.strip(',')+');'
            self.cmd.execute(cmdstr)
            self.curs.commit()
        else:
            print '重复'+dic['title']
    def check(self,dic,tablename):
        coloum=[]
        valu=[]
        cmd2=self.curs.cursor()
        cmdstr='''SELECT title,answer from '''+tablename+''' where title =='''+dic['title']
        cmd2.execute(cmdstr)
        result=cmd2.fetchall()
        cmd2.close()
        for i in result:
            if dic['answer']==i[1]:
                return True
        return False
    def commit(self):
        self.curs.commit()
        self.curs.close()
def SaveToSql(fpath):
    f=open(fpath).read()
    b=tiqu(f)
    if re.search(u'毛泽东思想',b.name):
        name='MaoGai'
    elif re.search(u'马克思主义',b.name):
        name='MaYuan'
    elif re.search(u'思想道德修养',b.name):
        name='SiXiu'
    elif re.search(u'中国近代史纲要',b.name):
        name='JinDaiShi'
    else:
        print "Error No Title File path is"+fpath
        name='Other'
    # type(b)
    c=sqlites(name)
    for i in b.dan:
        c.Idanxuan(i)
    for i in b.duo:
        c.Iduoxuan(i)
    for i in b.pan:
        c.Ipanduan(i)
    c.commit()
if __name__=='__main__':
    user=raw_input('Input user:')
    pwd=raw_input('Input passwd:')
    obj=szb(user=user,pwd=pwd)
    obj.get_word_to_file()
