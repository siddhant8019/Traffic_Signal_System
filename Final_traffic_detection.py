import torch, cv2 , threading, time,math
road_width = 36
avg_len ={'car_len_avg':4.5875,'bike_len_avg':2.1833,'bus_len_avg':12}
avg_width ={'bus':2.59,'car':1.768,'bike':0.81}
avg_acc ={'car_acc_avg':3.5,'bike_acc_avg':4,'bus_acc_avg':2.25}
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
lane1 = {'lane':1 ,'bicycle': 0, 'car': 0, 'motorcycle': 0, 'truck': 0, 'bus': 0}
lane2 = {'lane':2 ,'bicycle': 0, 'car': 0, 'motorcycle': 0, 'truck': 0, 'bus': 0}
lane3 = {'lane':3 ,'bicycle': 0, 'car': 0, 'motorcycle': 0, 'truck': 0, 'bus': 0}
lane4 = {'lane':4 ,'bicycle': 0, 'car': 0, 'motorcycle': 0, 'truck': 0, 'bus': 0}
laneturn=1

switcher = {
        0: lane1,
        1: lane2,
        2: lane3,
        3: lane4
    }
video1 = cv2.VideoCapture('\Desktop\opencv\\1.mp4')
video2 = cv2.VideoCapture('\Desktop\opencv\\2.mp4')
video3 = cv2.VideoCapture('\Desktop\opencv\\3.mp4')
video4 = cv2.VideoCapture('\Desktop\opencv\\4.mp4')

# video1 = cv2.VideoCapture('\Desktop\opencv\\5_1.mp4')
# video2 = cv2.VideoCapture('\Desktop\opencv\\5_2.mp4')
# video3 = cv2.VideoCapture('\Desktop\opencv\\5_3.mp4')
# video4 = cv2.VideoCapture('\Desktop\opencv\\5_4.mp4')

video1.get(10) #frame rate
video2.get(10)
video3.get(10)
video4.get(10)

vehicles = ['bicycle', 'car', 'motorcycle', 'truck', 'bus']


def detect(result, lane, lane_string, x, y):
    cv2.namedWindow(lane_string) #creating new window to show frames.
    cv2.moveWindow(lane_string,x,y) # fixing position of window
    result.display(render=True)  # to show the bounding boxes with probability.
    img = cv2.resize(result.imgs[0], (300,300))
    cv2.imshow(lane_string, img)
    all_object = result.pandas().xyxy[0].name.tolist() #Extracting count from DATAFRAME result
    for vehicle in vehicles:
         lane[vehicle] = all_object.count(vehicle)
    # print(lane_string," = ",lane)

def row_no(vehicle_count):
    total_vehicles_width = (2*(vehicle_count['bus']+vehicle_count['truck']) * avg_width['bus']) + (vehicle_count['motorcycle']* avg_width['bike']) + (
            vehicle_count['car']* avg_width['car'])
    rows = total_vehicles_width/road_width


    if rows!= 0: # just to avoid divide by 0 error
               return rows
    else:
               return rows+1


def calcTime(laneno):
    vehicle_count =switcher.get(laneno)
    rows = row_no(vehicle_count)
    motorcycle_count = vehicle_count['motorcycle'] / rows
    bus_count = 2*vehicle_count['bus'] / rows
    truck_count = 2*vehicle_count['truck'] / rows
    car_count = vehicle_count['car']/ rows
    cycle_count = vehicle_count['bicycle'] / rows
    # s = ut + 1/2 at^2

    total_bustruck_cnt = bus_count + truck_count
    total_mcycle_cnt = motorcycle_count + cycle_count


    bustruck_time = total_bustruck_cnt * (math.sqrt(( avg_len['bus_len_avg']) / avg_acc['bus_acc_avg'])) #avg len has been halved
    car_time = car_count * (math.sqrt((2 * avg_len['car_len_avg']) / avg_acc['car_acc_avg']))
    mcycle_time = total_mcycle_cnt * (math.sqrt((2 * avg_len['bike_len_avg']) / avg_acc['bike_acc_avg']))

    totaltime = bustruck_time + car_time + mcycle_time
    totaltime = totaltime * rows
    if totaltime > 120:
     totaltime = 12
    print('Time = ',totaltime)
    return totaltime


def traffic_count(video, lane, lane_string, x, y):
        while video.isOpened(): #Until video is open  read frames
            check, frame = video.read()
            #frame =cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
            if check:
                result = model(frame, size=400) # model will detect all objects and will store it in resut.
                detect(result, lane, lane_string, x, y)

            key = cv2.waitKey(1)
            if key == ord("q"): # if q typed then close the windows
                break
        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__" :
    # creating thread
    t1 = threading.Thread(target=traffic_count, args=(video1,lane1,'lane1',200,100))
    t2 = threading.Thread(target=traffic_count, args=(video2,lane2,'lane2',520,100))
    t3 = threading.Thread(target=traffic_count, args=(video3, lane3,'lane3',840,100))
    t4 = threading.Thread(target=traffic_count, args=(video4, lane4,'lane4',1160,100))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    count =100
    while True:
      print(switcher.get(laneturn))
      time.sleep(calcTime(laneturn))
      laneturn = (laneturn+1)%4

    t1.join()
    t2.join()
    t3.join()
    t4.join()