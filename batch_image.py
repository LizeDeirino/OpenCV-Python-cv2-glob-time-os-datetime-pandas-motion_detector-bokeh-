from cv2 import cv2
import glob

images=glob.glob("batch\\*.jpg")

for image in images:
    img=cv2.imread(image,0)
    re=cv2.resize(img,(100,100))
    cv2.imshow("Hey",re)
    cv2.waitKey(200)
    cv2.destroyAllWindows()
    cv2.imwrite(image+"_100.jpg",re)



# img=cv2.imread("galaxy.jpg",0)

#     resized_image=cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
#     cv2.imshow("Galaxy",resized_image)
#     cv2.imwrite("Galaxy_resized.jpg",resized_image)
#     cv2.waitKey(2000)
#     cv2.destroyAllWindows()