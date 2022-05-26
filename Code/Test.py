import cv2
import numpy as np

img_file = 'D:\Study\Python Codes\TemplateMatching\Data\\test.png'
img = cv2.imread(img_file, cv2.IMREAD_COLOR)           # rgb
alpha_img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED) # rgba
gray_img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)  # grayscale
#gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(type(img))
print('RGB shape: ', img.shape)        # Rows, cols, channels
print('ARGB shape:', alpha_img.shape)
print('Gray shape:', gray_img.shape)
print('img.dtype: ', img.dtype)
print('img.size: ', img.size)
print(img[112, 112])
print(alpha_img[112, 112])
print(gray_img[112, 112])
#blur = cv2.blur(img, (8, 8))
#cv2.imwrite('blurred.png', blur)
#dim = (int(img.shape[0]/2),int(img.shape[1]/2))
#res = cv2.resize(blur, dim, interpolation = cv2.INTER_AREA)
#cv2.imwrite('res.png', res)
#cv2.imwrite('gray.png',gray_img)
#img[45, 90] = [200,106,5]       # mostly blue
#img[173, 25] = [0,111,0]      # green
#img[145, 208] =  [0,0,177]    # red
#alpha_img[173, 25] = [0,111,0,255]    # opaque
#gray_img[173, 25] =  87                   # intensity for grayscale
