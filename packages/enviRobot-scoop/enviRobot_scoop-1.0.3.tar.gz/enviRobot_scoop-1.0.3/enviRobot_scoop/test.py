import enviRobot_scoop
str_input = '今天清晨六點左右，台中市的北屯區東光路550之11號，有回收廠的大量廢棄物發生了火警'
d, q, w = None, str_input, None
location = """{
"type": "coordinates",
"lat": 24.191,
"lon": 120.553
}"""
enviRobot_scoop.handle_enviRobot(d, q, w)