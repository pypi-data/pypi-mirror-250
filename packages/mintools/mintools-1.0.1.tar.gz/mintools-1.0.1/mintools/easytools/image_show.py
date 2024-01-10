import cv2
import matplotlib.pyplot as plt


def plt_imshow(images: list, axis_off=False):
    n = len(images)
    f = plt.figure()
    if axis_off:
        plt.axis("off")
    for i in range(n):
        # Debug, plot figure
        f.add_subplot(1, n, i + 1)
        plt.imshow(images[i])
    plt.show(block=True)


def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        img, gray, hsv = para  # 刚赋值时img是para[0]的引用，但是当给img重新赋值时，重新给a分配内存，不改变para[0]的值
        print('PIX:', x, y)
        print("BGR:", img[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])
        print("----------------------")


def opencv_imshow(winName, image):
    """
    通过鼠左键单击图片像素点，显示该像素点的坐标PIX[x, y],BGR值，灰度值，HSV值
    :param image: BGR image or gray image
    :return: None
    """
    gray = None
    hsv = None
    # BGR image
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # gray image
    elif len(image.shape) == 2:
        gray = image.copy()
        color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    para = [image, gray, hsv]
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(winName, mouse_click, para)
    while True:
        cv2.imshow(winName, image)
        k = cv2.waitKey(0)
        if k & 0xFF == ord('q') or k & 0xFF == 27:
            break
    cv2.destroyAllWindows()
