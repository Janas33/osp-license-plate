def find_plate(image_path):
    import cv2
    import numpy as np

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Blurowanie, aby pozbyć się szczegółów które nas nie interesują
    blur = cv2.bilateralFilter(gray, 11,90, 90)

    #Wykrywanie krawędzi
    edges = cv2.Canny(blur, 30, 200)

    #Znajdowanie konturów - krzywej która łączy punkty o tym samym kolorze albo nasyceniu
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()
    #-1 - wyrysuj wszystkie kontury
    image_contours = cv2.drawContours(image_copy, contours, -1, (255, 0, 0), 2)

    #Obliczmy jakie pola mają figury zakreślane przez kontury i wybieramy największe
    big_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    image_copy = image.copy()
    image_big_contours = cv2.drawContours(image_copy, big_contours, -1, (0, 0, 255), 2)

    plate = None
    for c in big_contours:
        print(type(c[0][0][0]))
        #Obliczamy długość krzywej zakreślanej przez kontur, True - zamknięty obszar
        perimeter = cv2.arcLength(c, True)
        #Sprawdzamy czy kontur jest prostokątem, zwraca listę z długościami każdego boku
        edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(edges_count) == 4:
            x,y,w,h = cv2.boundingRect(c)
            plate = image[y:y+h, x:x+w]
            break

    cv2.imwrite("plate.png", plate)
    #labret = np.array([x, y, w, h])
    a=234
    b=345
    c=435
    d=745
    #labret = [a, b, c, d]
    labret = [x, y, w, h]
    print(labret)
    print("siema")
    return labret


#import sys
#find_plate(sys.argv[1])

#import cv2
#image_path = "C:/Users/Krystian/Desktop/osp_test/tab2.jpg"
#image_path = "C:/Users/Krystian/Downloads/tab_test.jpg"
#image_path = "C:/Users/Krystian/PycharmProjects/OSP_license_plate/tab_test.jpg"
#find_plate(image_path)
