import tkinter
import json
import folium
from folium import plugins
from tkinter import *
import tkinter.ttk as exTk
import tkinter as tk
from tkhtmlview import HTMLLabel


# tạo biến có giá trị cực lớn để so sánh
MAX_VALUE = 999999


# đọc file
file = open('matrix.txt')
file.readline().split()
tsp = []
for i in file:
    x = list(map(float, i.split()))
    tsp.append(x)


def GTS1(tsp, start):
    cost = 0
    # tour ban đầu chỉ có địa điểm bắt đầu
    tour = [start]
    # đặt v là địa điểm bắt đầu
    v = start
    # lấy số lượng địa điểm có trong ma trận
    number_location = len(tsp)

    # tạo mảng để kiểm tra địa điểm đã thăm
    # gán tất cả các địa điểm = false <=> chưa thăm
    visited = [False for x in range(0, number_location)]
    # thăm địa điểm bắt đầu
    visited[start] = True

    # vòng lặp thăm qua tất cả các địa điểm
    while len(tour) < number_location:
        # gán chi phí nhỏ nhất bằng MAX_VLUE
        min_cost = MAX_VALUE
        # địa điểm tiếp theo tạm thời chưa có
        next_location = -1

        # tìm địa điểm kế tiếp mà địa điểm hiện hành đi đến có chi phí nhỏ nhất và chưa được thăm
        for i in range(0, number_location):
            # nếu i đã được thăm thì bỏ qua i xét địa điểm khác
            if visited[i]:
                continue
            # tìm thành phố kế tếp mà địa điểm hiện hành sẽ đi qua
            # gán chi phí nhỏ nhất bằng ch phí từ địa điểm hiện hành đến địa điểm kề
            if min_cost > tsp[v][i]:
                min_cost = tsp[v][i]
                next_location = i

        # cộng dồn chi phí mỗi khi qua thành phố mới
        cost = cost + tsp[v][next_location]
        # gán trạng thái cho địa điểm mơi = true <=> đã thăm
        visited[next_location] = True
        # gán địa điểm hiện hành bằng địa điểm kế tiếp để tiếp tục vòng lặp
        v = next_location
        # thêm địa điểm kề vừa đi qua vào đường đi
        tour.append(next_location)

    # cộng thêm chi phí từ địa điểm cuối đến địa điểm bắt đầu
    cost = cost + tsp[v][start]

    return cost, tour


def GTS2(tsp, p):
    # gán cost = vô cùng
    cost = MAX_VALUE
    # khởi tạo tour tốt nhất = rỗng
    best_tour = []
    k = 0
    while k < p:
        if cost > GTS1(tsp, k)[0]:
            cost = GTS1(tsp, k)[0]
            best_tour = GTS1(tsp, k)[1]
        k += 1

    return cost, best_tour


# đọc tất cả tên địa điểm và tọa độ trong file locations.json
locations_json = json.load(open('locations.json',  encoding='utf-8'))
locations = []
coordinates = {}
for i in locations_json:
    location = locations_json[i]['location']
    locations.append(location)
    coordinates[location] = (
        float(locations_json[i]['lat']), float(locations_json[i]['long']))


def getPoints(type):
    # lấy chi phí
    cost = 0
    map = folium.Map(location=[10.7773895, 106.6885525], zoom_start=12)
    # lấy giá trị combobox để chon địa điểm bắt đầu
    index = cbo.get()
    # nếu tên địa điểm vừa nhập có trong danh sách địa điểm thì thay tên địa điểm = vị trí để gọi thuật toán
    for i in range(len(locations)):
        if index == locations[i]:
            index = i

    # gọi lại thuật toán thêm vào tour
    tour = []

    if type == 1:
	    for i in GTS1(tsp, index)[1]:
	        tour.append(i)
	    cost = GTS1(tsp, index)[0]

    if type == 2:
	    for i in GTS2(tsp, len(locations))[1]:
	        tour.append(i)
	    cost = GTS2(tsp, len(locations))[0]

	

    # hiển thị tên địa điểm thay vì index
    for i in range(len(tour)):
        for j in range(len(locations)):
            # nếu ví trị j nào bằng với giá trị tour tại i
            # gán giá trị tour tại i bằng tên địa điểm tại j
            if j == tour[i]:
                tour[i] = locations[j]

    # tạo mảng chứa các tọa độ
    points = []
    for location in tour:
        points.append(coordinates[location])
    points.append(points[0])

    i = 1
    j = 1
    # tạo điểm đánh dấu từ tọa độ thứ 2 đến gần cuối
    while i < (len(tour)):
        while j < (len(points)-1):
            folium.Marker(points[j],
                          popup=tour[i],
                          tooltip=tour[i],
                          icon=plugins.BeautifyIcon(number=j,
                                                    border_color='blue',
                                                    border_width=1,
                                                    text_color='red'
                                                    )
                          ).add_to(map)
            i += 1
            j += 1

    # tạo điểm đánh dấu cho tọa độ xuất phát
    folium.Marker(points[0],
                  popup=tour[0],
                  tooltip=tour[0],
                  icon=folium.Icon(color='red', prefix='fa', icon='car')
                  ).add_to(map)

    # vẽ đường đi cho các điểm tọa độ
    folium.PolyLine(points,
                    color='blue',
                    weight=8,
                    ).add_to(map)

    # tạo chuỗi str để hiển thị lộ trình
    str = ''
    for i in range(len(tour)):
        str = str + ' ' + tour[i] + ' ->'
    str = str + ' ' + tour[0]

    # hiển thị lộ trình và chi phí lên trang html
    map.get_root().html.add_child(folium.Element("""
    <div style="position: fixed; 
        top: 50px; left: 70px; width: 700px; height: 100px; 
        background-color:white; border:2px solid grey;z-index: 900;">
        <h5>Lộ trình: {}</h5>""".format(str) + """
        <h5>Chi phí: {:.3f} km</h5>""".format(cost) + """
    </div>
    """))

    map.save('map.html')


# tạo cửa sổ tkinter
root_tk = tkinter.Tk()
root_tk.title("Thuật toán GTS")
cbo = exTk.Combobox(root_tk, width=30, font='Times 30', state='readonly')
cbo['value'] = locations
cbo.current(0)
btnChonGTS1 = Button(root_tk, text='Thực hiện GTS1', font='Times 30',
                 command=lambda:getPoints(1))
btnChonGTS2 = Button(root_tk, text='Thực hiện GTS2', font='Times 30',
                 command=lambda:getPoints(2))
lblShowMap = HTMLLabel(root_tk,  html='<a href="map.html">Xem bản đồ</a>')

cbo.grid(row=0, column=0)
btnChonGTS1.grid(row=0, column=1)
btnChonGTS2.grid(row=1, column=1)
lblShowMap.grid(row=2, column=0)

root_tk.mainloop()
