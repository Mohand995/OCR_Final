import cv2
import shutil
import os
import pytesseract
import numpy as np
import json
import requests 
from io import BytesIO
from PIL import Image
################################################################################################################################

def Run(image_path,api=True):
    #pytesseract.pytesseract.tesseract_cmd='/app/.apt/usr/bin/tesseract'
   # if os.path.exists("/app/ara_number_id.traineddata"):
          # shutil.move("/app/ara_number_id.traineddata", "./.apt/usr/share/tesseract-ocr/4.00/tessdata/ara_number_id.traineddata")
            
    if api:
        image=url_to_img(image_path)
    else :
        image =cv2.imread(image_path)

    name,Address=Extract_name(image)
    ID=Extract_ara_ID(image)

    DOB=Extract_DOB(image)
    eng_no=extract_eng_num(image)

    result={"name":name ,
           "ID":ID,
           "Address": Address,
           "DOB":DOB , 
           "Eng_Code":eng_no}
    return result
#############################################################################################################

def Extract_ara_ID(img):

    img = Crop_ROI_ID(img)
    copy=img

    count = 0
    while (True):
        count = count + 1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)
        res = pytesseract.image_to_string(img, lang="ara_number_id").split()
        if res != []:
            for i in res:
                if len(i) > 13 and len(i) < 15 and i[0]==enToArNumb(2):
                    return  i

        f_res=""
        for i in range(1,len(res)+1):
            if i >1:
                temp=res[len(res) - i]
                temp+=f_res
                f_res = temp
            else:
                f_res+= res[len(res) - i]

            if len(f_res)==14:
                
                return f_res


        img = increase_contrast(copy)
        if count > 1:
            img = increase_contrast(img)
        if count == 3:
            return "please re-capture the image"
        continue


############################################################################################

def Extract_name(img):
    img = Crop_ROI_Name(img)
    img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    _,img = cv2.threshold(img, 90, 255, cv2.THRESH_TRUNC)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    res = pytesseract.image_to_string(img, lang="ara").split()
    print(res)
    if res==[]:
        print("recapture image")
    else:
        name=str(res[0])+' '+str(res[1])+' '+str(res[2])
        Address=str(res[3])+' '+str(res[4])+' '+str(res[5])+' '+str(res[6])
        return name , Address

#############################################################################################
def Extract_DOB(img):
        ID=Extract_ara_ID(img)
        DOB=str(ID[1:3])+'/'+str(ID[3:5])+'/'+str(ID[5:7])
        return DOB
########################################################################################################

def extract_eng_num(img):
    
    img =Crop_ROI_Eng_No(img)
    copy=img
    count=0
    while(True):
            img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = detect_digit_only(img).split()
            if res != []:
                for i in res:
                    if len(i)>6:
                        return (i[len(i) - 7:])

            res = pytesseract.image_to_string(img, lang="eng").split()
            c_res=[]
            if res != []:
                for i in res:
                    if len(i) > 6:
                        c_res = i
                        break

            if (len(c_res) > 6):
                ch=0
                for i in c_res:
                    if i.isalpha():
                        ch=ch+1
                        break
                    else:
                        continue
                if ch>0:
                    ""
                else:
                    return (c_res[len(c_res) - 7:])


            img = increase_contrast(copy)
            if count>1:
                img = increase_contrast(img)
            if count==3:
                return "please re-capture the image"
            continue

#########################################################################################################

def increase_contrast(img):

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final
####################################################################################################

def Crop_ROI_ID(img):
    width = 712
    height = 512
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    h,w,ch=img.shape
    img = img[int(h*0.6):int(h/1.09), int(w/2.8):int(w/1)]

    return img
################################################################################################

def Crop_ROI_Name(img):
    width = 712
    height = 512
    dim = (width, height)

    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)	
    h,w,c=img.shape
    img=img[int(h*0.20):int(h*0.75),int(w/2):int(w/1)]

    return img
####################################################################################################

def Crop_ROI_Eng_No(img):
    width = 712
    height = 512
    dim = (width, height)

    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)	
    h,w,c=img.shape
    img = img[int(h/2):int(h), int(w/12.5):int(w/2.5)]
    return img

#############################################################################
def enToArNumb(number):
    english_to_arabic = {'1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩', '0': '٠'}
    return english_to_arabic.get(number)

 #########################################################################################   
def ArToEnNumb(number):
    arabic_to_english = {'١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '٠': '0'}
    return arabic_to_english.get(number)

 ##############################################################################

def detect_digit_only(img):
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    res=pytesseract.image_to_string(img, config=custom_config)
    return res

###################################################################################################

def url_to_img(url, save_as=''):
  img = Image.open(BytesIO(requests.get(url).content))
  if save_as:
    img.save(save_as)
  return np.array(img)

  ##################################################################################

if __name__ == '__main__':
    
    Run('https://i.ibb.co/kGzHGRP/index.jpg')
