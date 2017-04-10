#coding=utf-8
# this is a server which accept traffic report and video data
# video data, format mp4
# report info:
# name
# phone number
# ID number:
# address:
# time: 20xx-xx-31 14:45
# template: 省份 number
# plate color: 蓝色 黄色 其他
# behavior: 实线变道, 违法占用公交专用道,机动车闯红灯,车窗抛物,
#           不避让特种车辆,货运车占客车道,机动车逆向行驶,
#           车辆行驶过程中发生的其他行为,货车上高架
#


from flask import Flask,request,redirect,render_template
from werkzeug import secure_filename
from enum import Enum
import json
app = Flask(__name__)
FILE_DIR="video_data/"
@app.route("/upload_file",methods=['POST','GET'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
@app.route("/upload_info",methods=['POST','GET'])
def upload_info():
    if request.method == 'GET':
        return render_template('submit.html')
    elif request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        id = request.form['id']
        address = request.form['address']
        time = request.form['time']
        provence = request.form['provence']
        pnumber = request.form['plate_number']
        pcolor = request.form['plate_color']
        bhav = request.form['behavior']

        info = ReportInfo(name,phone,id,address,time,provence,pnumber,pcolor,bhav)
        f = request.files['file']
        f.save(FILE_DIR+secure_filename(f.filename))
        return "get Info: \n"+info.toJSON()



class ViolationBehavior(Enum):
    NONE = -1
    BIAN_DAO= 1 #实线变道,
    ZHAN_GONG =2 # 违法占用公交专用道,
    HONG_DENG = 3 # 机动车闯红灯,
    PAO_WU = 4 # 车窗抛物,
    BUBI_RANG = 5 #不避让特种车辆,
    ZHAN_KE = 6 # 货运车占客车道,
    NI_XIANG = 7 # 机动车逆向行驶,
    QI_TA = 8 #车辆行驶过程中发生的其他行为,
    HUOCHE_GAOJIA = 9 # 货车上高架

class ReportInfo:
    def __init__(self, name, phonenumber, id_number):
        self.name = name
        self.phone = phonenumber
        self.id = id_number
        self.address = None
        self.time = None
        self.provence = None
        self.plate_number = None
        self.plate_color = None
        self.behavior = -1

    def __init__(self, name, phonenumber, id_number,address,time,provence,pnumber,pcolor,bhav):
        self.name = name
        self.phone = phonenumber
        self.id = id_number
        self.address = address
        self.time = time
        self.provence = provence
        self.plate_number = pnumber
        self.plate_color = pcolor
        self.behavior = bhav

    def setAddress(self,address):
        self.address = address
    def getAddress(self):
        return self.address

    def setTime(self,time):
        self.time = time
    def getTime(self):
        return self.time

    def setProvence(self,provence):
        self.provence = provence
    def getProvence(self):
        return self.provence

    def setPlateNumber(self,plate_number):
        self.plate_number = plate_number
    def getPlateNumber(self):
        return self.plate_number

    def setPlateColor(self,color):
        self.plate_color = color
    def getPlateColor(self):
        return self.plate_color

    def setBehavior(self,behav):
        self.behavior = behav
    def getBehavior(self):
        return self.behavior

    def toJSON(self):
        return json.dumps(self,default=lambda o:o.__dict__)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002,debug=True)
    info = ReportInfo("kyle","34234234","34234","address","time","hu","232342342","lan",123)
    print info.toJSON()
