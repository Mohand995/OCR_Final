import cv2
import shutil
import pytesseract
#import preprocessing

def Run(image_path):
    image=cv2.imread(image_path)
    pytesseract.pytesseract.tesseract_cmd='/app/.apt/usr/bin/tesseract'
    shutil.move("/app/ara_number_id.traineddata", "./.apt/usr/share/tesseract-ocr/4.00/tessdata/ara_number_id.traineddata")
    name=Extract_name(image)
    ID=Extract_ara_ID(image)
    print("Name : {}".format((name)))
    print("ID : {}".format(ID))
    return name,ID

def Extract_ara_ID(img):

    img = Crop_ROI_ID(img)
    copy=img

    count = 0
    while (True):
        count = count + 1
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)

        res = pytesseract.image_to_string(img, lang="ara_number_id").split()
        print(res)
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
    _,img = cv2.threshold(img, 90, 255, cv2.THRESH_TRUNC)

    res = pytesseract.image_to_string(img, lang="ara").split()
    print(res)
    if res==[]:
        print("recapture image")
    else:
        name=str(res[0])+' '+str(res[1])
        return name




def increase_contrast(img):

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final


def Crop_ROI_ID(img):
    width = 712
    height = 512
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    h,w,ch=img.shape
    img = img[int(h/1.8):int(h/1.09), int(w/2.8):int(w/1)]

    return img


def Crop_ROI_Name(img):
    width = 712
    height = 512
    dim = (width, height)

    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)	
    h,w,c=img.shape
    img=img[int(h*0.22):int(h*0.75),int(w/2):w]

    return img


def enToArNumb(number):
    dic = {
        0:'۰',
        1:'١',
        2:'٢',
        3:'۳',
        4:'۴',
        5:'۵',
        6:'۶',
        7:'۷',
        8:'۸',
        9:'۹',
    }
    return dic.get(number)




if __name__ == '__main__':
    #image=preprocessing.extractIdCard("9.jpg")
    Run("9.jpg")
