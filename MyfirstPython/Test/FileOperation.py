# import cv2
# fn='C:\\Users\\Administrator\\Desktop\\picture1.jpg'
# img=cv2.imread(fn)
# cv2.imshow('eee',img)
# cv2.waitKey()
import os
import shutil
dir_path = 'C:\\Users\\Administrator\\Desktop\\'
filename='test.txt'
fullpath = os.path.join(dir_path,filename)
if(os.path.exists(fullpath)):
    print('存在该路径')
    if(os.path.isdir(fullpath)):
        print('这是一个目录')
        print(os.path.split(fullpath)[0]+'下的所有文件')
        for name in os.listdir(path=dir_path):
            print(os.path.join(dir_path,name))
    elif(os.path.isfile(fullpath)):
        print('这是一个文件')
        f=open(fullpath,'w')
        f.write('该文件绝对路径'+fullpath)
        f.close()
        f=open(fullpath,'r')
        text = f.readlines()
        print('文件内容')
        for line in text:
            print(line,'文件长度',len(line))
        f.close();
    else:
        print('这既不是目录也不是文件')
else:
    print('不存在该路径')
    os.mkdir(fullpath)
    print('创建成功')