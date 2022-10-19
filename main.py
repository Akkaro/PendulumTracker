"""
Marton Szabolcs & Benő Ákos
Matematikai inga követése és elemzése, ideális és reális esetekben
2021.01.15
"""

import cv2
import time
import math


rout: str =r"C:\Users\Akos\Downloads\Fizika5.mp4"
tracker = cv2.TrackerCSRT_create()
v = cv2.VideoCapture(rout)

point_array = ()
center = 0
center_before = 0
going_left = False
going_right = False
start_time = 0
end_time = 0

maxi = 0
mini = 0
counter = 0
total_lenght_max = 0.0000
total_lenght_min = 999999.99999999
total_way = 0
g = 9.81

# fps számláló változói
prev_frame_time = 0
new_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX
total_fps = 0
counter_2 = 0

#első képkocka leválasztása
def getFirstFrame(videofile):
    vidcap = cv2.VideoCapture(videofile)
    success, frame = vidcap.read()
    if success:
        return frame
    return 0


img = getFirstFrame(rout)
img_2 = getFirstFrame(rout)
img_3 = getFirstFrame(rout)

#egy clickre történő reakció
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image1', img)
        point = (x, y)
        global point_array
        point_array += point

    return


def click_event_cord(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_3, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image3', img_3)
        point = (x, y)
        global point_array
        point_array += point

    return

#a piros vonal behúzása
def line():
    cv2.line(img, (int(point_array[0]), int(point_array[1])), (int(point_array[2]), int(point_array[3])),
             (0, 0, 255), 2)
    cv2.imshow('image2', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#zsinór végeinek megjelelölése
def cord(img_3):
    print('Jelöld be az inga zsinórjának két végét')
    cv2.imshow('image3', img_3)
    cv2.setMouseCallback('image3', click_event_cord)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#koordinatak
def point(img):
    cv2.imshow('image1', img)
    cv2.setMouseCallback('image1', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#referenciatavolság kiszámítása
def calculate_reference(point_array):
    d = math.sqrt(((point_array[2] - point_array[0]) ** 2) + ((point_array[3] - point_array[1]) ** 2))

    data = input('Add meg a referenciatávolságot:')
    data = int(data)
    global const_cm
    const_cm = data / d

#zsinór hosszának kiszámítása
def calculate_cord_lenght(point_array):
    global cord_lenght
    cord_lenght = math.sqrt(
        ((point_array[6] - point_array[4]) ** 2) + ((point_array[7] - point_array[5]) ** 2)) * const_cm

#előre modelezett lassulás
def slow():
    total_lenght_difference = total_lenght_max - total_lenght_min
    lenght_minus_turn = total_lenght_difference / counter
    print('Hozzávetőlegesen', int(total_lenght_min / lenght_minus_turn), 'periódus múlva megállt volna az inga')
    print('lenght difference', total_lenght_difference, 'counter', counter)

#ideális inga képletei
def kepletek():
    print('Amennyiben az inga ideálisnak tekinthető a következő számítások végezhetőek el:')
    l=cord_lenght/100
    frekvencia= (1/math.pi)*math.sqrt(g/l)
    periodus = (2*math.pi)*math.sqrt(l/g)
    korfrekvencia = math.sqrt(g/l)
    print('Periódus:', periodus, 'sec')
    print('Frekvencia:', frekvencia, 'Hz')
    print('Körfrekvencia:', korfrekvencia, 'Hz')


point(img)
line()
calculate_reference(point_array)
cord(img_3)
calculate_cord_lenght(point_array)

print('A zsinór hossza:',cord_lenght)

kepletek()

print('Jelöld be a lekövtni kívánt tárgyat (az inga mozgó részét)!')

ret, frame = v.read()
cv2.imshow('Frame', frame)
bb = cv2.selectROI('Frame', frame)
tracker.init(frame, bb)

#a program alapja, mely eldönti hogy a követett tárgy milyen irányba megy, és hogy mikor ér periódusa szélére
def intez(newcenter, center, going_left, going_right, start_time, end_time, center_before, maxi, mini,
          counter, total_lenght_max, total_lenght_min, total_way):
    if newcenter == center or newcenter == center_before:
        return going_left, going_right, start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way

    if newcenter < center < center_before:
        going_left = True
        # print('going_left')
        if start_time == 0:
            start_time = time.time()
        if going_right == True:
            maxi = center_before
            if center_before < newcenter or mini == 0:
                going_right = False
                return going_left, going_right, start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way
            print("Legnagyobb: ", center_before)


            total_lenght = (maxi - mini) * const_cm
            if total_lenght > total_lenght_max:
                total_lenght_max = total_lenght
            if total_lenght < total_lenght_min:
                total_lenght_min = total_lenght
            print('total lenght', total_lenght, 'cm')
            total_way += total_lenght
            counter += 1
            going_right = False
            going_left = True
            end_time = time.time()
            fulltime = end_time - start_time
            print('fulltime', fulltime, 'sec')
            start_time = time.time()

    if newcenter > center > center_before:
        going_right = True
        # print('going_right')
        if start_time == 0:
            start_time = time.time()
        if going_left:
            mini = center_before
            if center_before > newcenter or maxi == 0:
                going_left = False
                return going_left, going_right, start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way
            print("Legkisebb: ", center_before)


            total_lenght = (maxi - mini) * const_cm
            if total_lenght > total_lenght_max:
                total_lenght_max = total_lenght
            if total_lenght < total_lenght_min:
                total_lenght_min = total_lenght
            print('total lenght', total_lenght, 'cm')
            total_way += total_lenght
            counter += 1
            going_left = False
            going_right = True
            end_time = time.time()
            fulltime = end_time - start_time
            print('fulltime', fulltime, 'sec')
            start_time = time.time()

    return going_left, going_right, start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way


total_time_start = time.time()
start = time.time()
#ciklus mely képkockákra szedi, és elemzi a videót
while True:
    ret, frame = v.read()
    if not ret:
        break
    (success, box) = tracker.update(frame)

    if success:

        (x, y, w, h) = [int(a) for a in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cor_1 = int(x + w / 2)
        cor_2 = int(y + h / 2)
        cv2.line(frame, (cor_1, cor_2), (cor_1 + 1, cor_2 + 1), (0, 0, 255), 2)
        newcenter = int(x + w / 2)

        going_left, going_right, start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way = intez(
            newcenter, center, going_left, going_right,
            start_time, end_time, center_before, maxi, mini, counter, total_lenght_max, total_lenght_min, total_way)

        if newcenter != center:
            center_before = center
            center = newcenter

    #élő fps számláló
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    total_fps += fps
    counter_2 += 1
    fps = str(fps)
    cv2.putText(frame, fps, (0, 30), font, 1, (100, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(5) & 0xff
    if key == ord('q'):
        break

#végső számítások
total_time_end = time.time()
total_time = total_time_end - total_time_start
original_time = total_time / 4
speed = (total_way/100) / (total_time/original_time)
print('A labda átlagsebessége', speed, 'm/s')
print('total_time', total_time)
slow()
average_fps = total_fps / counter_2
print('atlag fps', average_fps)

v.release()
cv2.destroyAllWindows()
