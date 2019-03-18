# __author__='lijishuang'
#-*- coding:utf-8 -*-

# 倒入相应的包是为了支持以下几个过程：
# 1.PIL.image :是支持图像的采集的过程，我们要识别的内容都是以图像的形式进行的保存，因此需要诸如图像的导入和导出的过程的支撑，这个包的作用就是支撑这个过程的；
# 2.convert的转换的格式需要进行相应的确认：参数P和参数L的效果是不一致的，需要进行实验说明
# 3.将一个包含多个字符的验证码切割成单个字符进行训练集的构造
# 4.进行相应的训练的过程，用train的过程进行训练
# 5.基本向量空间搜索引擎:利用相同维度下，比较两向量的余弦夹角来判断两个向量之间的相似度。这就是向量空间搜索理论
from PIL import Image
import math,os,string,hashlib,time
from matplotlib import pyplot as plt
import numpy as np
from operator import itemgetter
import shutil

class loons(object):
    def __init__(self,fp):
        # 类的初始化函数，这个函数的作用是把图片加载到这个类中，并进行一个简单的处理过程
        # 1.打开图片使用open的方法打开
        # 2.把图片转换成黑白图片内容
        # 3.创建一个新的图片大小和原始图片一致，颜色默认为8-bit彩色的形式
        self.im = Image.open(fp)
        self.im.convert("P")
        self.im2=Image.new("P",self.im.size,255)
        self.v=self.VectorCompare()
    def convert_two_pic(self,pix=[],fp=None):
        # 分析图片的颜色索引值
        # 实现图像的转换的过程，把图像转换成
        # 传入参数说明：
            # pix:得到的需要过滤的像素的值
            # fp:重命名图像的名字
            for x in range(self.im.size[0]): #行
                for y in range(self.im.size[1]): #列
                    if self.im.getpixel((x,y)) in pix:
                        self.im2.putpixel((x,y),0)
            if fp != None:
                self.im2.save(fp+".gif")
            self.im2.show()
    def conver_one_pic_1(self,im21,fp=None):
        # 纵向切割图片，切割成单个字符就可以进行机器学习的训练集合了,使用crop函数对图片进行切割
        # 按照区域的大小进行相关的切割操作，需要构造矩形进行操作
        startbool=False
        endbool=False
        start_x=0
        start_y=0
        end_x=0
        end_y=0
        for x in range(im21.size[0]):
            # 去除多余的255（白色）的像素的值
            for y in range(im21.size[1]):
                if startbool== False:
                    if im21.getpixel((x,y)) == 0:
                        start_x=x 
                        startbool=True
                if im21.getpixel((x,y)) == 0:
                        end_x=x 
        for y in range(im21.size[1]):
            for x in range(im21.size[0]):
                if endbool== False:
                    if im21.getpixel((x,y)) == 0:
                        start_y=y 
                        endbool=True
                if im21.getpixel((x,y)) == 0:
                        end_y=y 
        # print start_x,end_x,start_y,end_y  # 6 66 8 20
        # print self.im2.size[0]  # 84
        # print self.im2.size[1]  # 22
        # 结果集合为相对以im2的坐标的结果
        im_new=im21.crop((start_x,start_y,end_x+2,end_y+1)) #加二的情况是因为end是结束的部分，不包括end+2的那行，但是需要最后一行是全白，所以加2
        # im_new.show()
        return im_new ,start_x,end_x, start_y,   end_y
        # im_new.save('new.gif','gif')
    def conver_one_pic_2(self,fp=None):
        # 切分出单个字符进行训练集的准备工作
        inbool=False
        outbool=False
        start=0
        end=0
        pix_patch=[]
        image_news ,start_x,end_x,start_y,end_y= self.conver_one_pic_1(self.im2)
        for x in range(image_news.size[0]):
            for y in range(image_news.size[1]):
                pix=image_news.getpixel((x,y))
                if pix!=255:
                    inbool= True
            if inbool==True and outbool==False:
                outbool=True
                start=x
            if inbool==False and outbool==True:
                outbool=False
                end=x
                pix_patch.append((start+start_x,start_y,end+start_x,end_y))
            inbool=False
        # print pix_patch
        return pix_patch

    def Train(self):
        # 输入训练集合进行相应的训练，使用向量空间搜索的算法是因为可以计算相似度，而且比较次数是可以在训练之前获悉的
        # 1.训练的第一步是去除白噪声；我们的训练集合虽然是白色背景黑色的底不需要进行去噪声的过程，但是现实情况下是需要进行去除噪声的处理的
        # 2.构造相应的向量空间
        # OverZoom()
        icons=[i for i in (string.digits+string.ascii_lowercase)] # 生成一个长的字符串：1234567890abcdefg...的全部，对应的是训练集的相应的文件
        # 加上去边的操作
        # 需要对训练的图片进行相应的切割的操作
        count=1000
        imageset=[]
        boolstatus=False
        for case in icons:
            # 先删除转换的目录在进行重新创建的工作
            if os.path.exists("res/%s"%(case)) is False:
                os.makedirs("res/%s"%(case))
            else:
                shutil.rmtree("res/%s"%(case))
                os.makedirs("res/%s"%(case))
            # 每一个字符进行遍历的操作
            for img in os.listdir('iconset/%s/'%(case)): # pyloons/iconset
                tmp=[]
                if img != "Thumbs.db" and img != ".DS_Store":                   
                    t_img=Image.open("iconset/%s/%s"%(case,img))
                    new_img,start_x,end_x,start_y,end_y=self.conver_one_pic_1(t_img)
                    new_img_1=new_img.crop((0,0,new_img.size[0]-1,new_img.size[1]))
                    new_img_1.save("res/%s/%s.gif"%(case,count),"gif")
                    tmp.append(self.OverZoom(new_img_1)) #  去噪声的处理
                imageset.append({case:tmp})
                count+=1
        return imageset
    def Computer(self,testset,trainset):
        # 测试图片和训练图片进行计算得到输出的结果
        result =[]
        for test in testset:
            print test
            im3=self.im2.crop((test[0],test[1],test[2],test[3]))
            # im3.show()
            guess=[]
            for train in trainset:
                for x,y in train.iteritems():
                    # print x,y
                    if len(y)!=0:
                        res = self.v.selfAdd(y[0],self.OverZoom(im3))
                        guess.append((res,x))
            # print self.OverZoom(im3)
            guess.sort(reverse=True,key=itemgetter(0))
            # print guess
            result.append(guess[0])
        return result
    def OverZoom(self,im):
        # 对需要识别的图片进行去噪过程,统计出现的次数和相应的像素的值:(出现的次数，像素值)
        # dict={}
        # mid_num=im.histogram()
        # for data in enumerate(mid_num):
        #     dict[data[0]]=data[1]
        # return dict

        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        # print d1
        return d1
    
    class VectorCompare(object):
        # 计算向量空间的分子和分母
        
        def selfAddDown(self,im):
            total=0
            for key,count in im.iteritems():
                total = total+count**2
            return math.sqrt(total)
        
        def selfAdd(self,im1,im2):
            up=0
            result=0
            for word,count in im1.iteritems():
                if im2.has_key(word):
                    up +=count*im2[word]
            a=self.selfAddDown(im1) 
            b=self.selfAddDown(im2)
            result=up/(a*b)
            return result
                

    def run(self):
        # 识别过程的主体过程，其中的整体的逻辑的调用的过程都是这个函数的调用的过程
        # 第一步：验证码图像的预处理过程，得到训练的数据值，把彩色的图片转换层黑白的图片，图片的值取【0，255】之间的数字
        self.convert_two_pic([220,227])
        tests=self.conver_one_pic_2()
        images=self.Train()
        res=self.Computer(tests,images)
        print res
        
class catch_histogram(object):
    def __init__(self,image):
        self.im3=Image.open(image)
        
    # 统计图像的的颜色直方图的中颜色出现的概率的情况
    def HisToGram(self,fp=None):
        mid=self.im3.convert("P").histogram()
        # print mid
        n, bins, patches = plt.hist(np.array(self.im3.convert("P")).flatten(), bins=256, normed=0, facecolor='green', alpha=0.75,hold=1)
        # plt.show()
        # 输出相应的高概率的相应的颜色值
        # 使用了两个函数进行处理：
        #       enumerate:python内置的函数，其作用就是把可遍历的对象连同下标构造出一个数据结果：（数据下标，数据）；
        #       itemgetter：来自operator的模块，作用是于获取对象的哪些维的数据，参数为一些序号；
        #       reverse：为True的时候为降序排列；
        print sorted(enumerate(mid),key=itemgetter(1),reverse=True)
    # 找到可以识别像素的相关的颜色值
    def Find_only_pix_pic(self,pix=[],fp=None):
        # 目的是把在图片内的相应的干扰都去除掉，使只尽量的包含需要识别的部分
        # pix：为需要测试的像素值
        find_pic=self.im3.convert("P")
        find_pix_pic = Image.new("P",self.im3.size,255)
        for x in range(find_pic.size[1]):
            for y in range(find_pic.size[0]):
                if find_pic.getpixel((y,x)) in pix:
                    find_pix_pic.putpixel((y,x),0)
        find_pix_pic.show()
        find_pix_pic.save('222.gif','gif')


if __name__ == "__main__":
    # 主函数的调用，其实现的逻辑显示的是通过调用类loons的函数实现导入图片和执行检测的过程
    # 进行确认颜色索引值的过程
    # ct=catch_histogram("pic.gif")
    # ct.HisToGram()
    # 确定下哪些像素是在需要识别的数字上的像素值
    # 220的像素值处理后的效果很明显
    # ct.Find_only_pix_pic([220,227])

    vc = loons("pic.gif")
    vc.run()