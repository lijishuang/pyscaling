# 识别验证码的小程序

## 识别要求
 - 只能识别数字和字母的组合，而且是排列正规的验证码
 - 识别过程中使用的是基本向量空间搜索引擎
 - 使用python进行程序的编写
  
## 识别过程

### 整体的框架

- 整体程序分为两个大类：loons和catch_histogram
- loons：
  - 程序进行识别和处理的部分
- catch_histogram：
  - 进行相应的颜色直方图统计的类，目的是找到相应的颜色索引值
  
### 具体的实现流程

#### 第一步：
确定相应的颜色索引值：
```
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
```
执行函数：
```
      ct=catch_histogram("pic.gif")
      ct.HisToGram()
```
得到的相关内容结果如下：
```
[(255, 625), (212, 365), (220, 186), (219, 135), (169, 132), (227, 116), (213, 115), (234, 21), (205, 18), (184, 15), (241, 10), (248, 10), (191, 8), (198, 6), (155, 3), (157, 3), (158, 3), (167, 3), (228, 3), (56, 2), (67, 2), (91, 2), (96, 2), (109, 2), (122, 2), (127, 2), (134, 2), (140, 2), (168, 2), (176, 2), (200, 2), (211, 2), (240, 2), (242, 2), (247, 2), (43, 1), (44, 1), (53, 1), (61, 1), (68, 1), (79, 1), (84, 1), (92, 1), (101, 1), (103, 1), (104, 1), (107, 1), (121, 1), (126, 1), (129, 1), (132, 1), (137, 1), (149, 1), (151, 1), (153, 1), (156, 1), (165, 1), (170, 1), (171, 1), (175, 1), (186, 1), (188, 1), (192, 1), (197, 1), (206, 1), (207, 1), (208, 1), (209, 1), (210, 1), (215, 1), (223, 1), (235, 1), (236, 1), (253, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0), (41, 0), (42, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0), (51, 0), (52, 0), (54, 0), (55, 0), (57, 0), (58, 0), (59, 0), (60, 0), (62, 0), (63, 0), (64, 0), (65, 0), (66, 0), (69, 0), (70, 0), (71, 0), (72, 0), (73, 0), (74, 0), (75, 0), (76, 0), (77, 0), (78, 0), (80, 0), (81, 0), (82, 0), (83, 0), (85, 0), (86, 0), (87, 0), (88, 0), (89, 0), (90, 0), (93, 0), (94, 0), (95, 0), (97, 0), (98, 0), (99, 0), (100, 0), (102, 0), (105, 0), (106, 0), (108, 0), (110, 0), (111, 0), (112, 0), (113, 0), (114, 0), (115, 0), (116, 0), (117, 0), (118, 0), (119, 0), (120, 0), (123, 0), (124, 0), (125, 0), (128, 0), (130, 0), (131, 0), (133, 0), (135, 0), (136, 0), (138, 0), (139, 0), (141, 0), (142, 0), (143, 0), (144, 0), (145, 0), (146, 0), (147, 0), (148, 0), (150, 0), (152, 0), (154, 0), (159, 0), (160, 0), (161, 0), (162, 0), (163, 0), (164, 0), (166, 0), (172, 0), (173, 0), (174, 0), (177, 0), (178, 0), (179, 0), (180, 0), (181, 0), (182, 0), (183, 0), (185, 0), (187, 0), (189, 0), (190, 0), (193, 0), (194, 0), (195, 0), (196, 0), (199, 0), (201, 0), (202, 0), (203, 0), (204, 0), (214, 0), (216, 0), (217, 0), (218, 0), (221, 0), (222, 0), (224, 0), (225, 0), (226, 0), (229, 0), (230, 0), (231, 0), (232, 0), (233, 0), (237, 0), (238, 0), (239, 0), (243, 0), (244, 0), (245, 0), (246, 0), (249, 0), (250, 0), (251, 0), (252, 0), (254, 0)]
```

#### 第二步
根据选择的颜色索引值进行识别，选择的过程为先选择前10个出现次数最高的
```
(255, 625), (212, 365), (220, 186), (219, 135), (169, 132), (227, 116), (213, 115), (234, 21), (205, 18), (184, 15), (241, 10)
```
在其中进行相应的设置，这里采用的是实验每一个像素的值，结果发现在220和227的值的时候其效果是最好的，能很好的分辨出数字来进行处理；

紧接着进行下一个过程，用选择出来的像素的索引值对原始图片进行转换：
```
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
```
转换的结果就是如果在原始的图片中像素就是索引像素的值，则这个像素的值变成0（黑色），否则就按照初始化的过程变成：self.im2=Image.new("P",self.im.size,255)白色的值；

#### 第三步
紧接着就是对图片需要识别的图片进行切割的过程，切割的过程分为两个步骤进行：

##### 第一个过程：conver_one_pic_1
```
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
```
此过程是实现的对需要检测的样本进行分割，确定每一个需要识别的形状的坐标，这个过程在后续的对样本库中的样本切割的过程同样适用；

##### 第二个过程：conver_one_pic_2
```
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
```
获取识别的坐标的，切分出单个字符进行训练集的准备工作

#### 第四步

基本向量空间搜索算法实现：
```
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
```

#### 第五步

计算的过程：计算测试的图片和图片库中的图片的相似度，值越大则代表越相似。
```
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
```

#### 第六步
训练的过程
```
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
```
### 整体的训练过程
def run(self):
        # 识别过程的主体过程，其中的整体的逻辑的调用的过程都是这个函数的调用的过程
        # 第一步：验证码图像的预处理过程，得到训练的数据值，把彩色的图片转换层黑白的图片，图片的值取【0，255】之间的数字
        self.convert_two_pic([220,227])
        tests=self.conver_one_pic_2()
        images=self.Train()
        res=self.Computer(tests,images)
        print res

### 在主函数中的识别过程
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
### 最终的效果
```
(base)    ~/Desktop/MachineLearning/100DAY/pyScaling   master ●✚  python loons.py 
(6, 8, 14, 20)
(15, 8, 25, 20)
(27, 8, 35, 20)
(37, 8, 46, 20)
(48, 8, 56, 20)
(57, 8, 67, 20)
[(0.9137931034482759, '7'), (0.8988216489544953, 's'), (0.8051091587951025, '9'), (0.9593813007189699, 't'), (0.9072221051385092, '9'), (0.875760539039714, 'j')]
(base)   ~/Desktop/MachineLearning/100DAY/pyScaling   master ●✚  
```
