from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import re
from pyecharts import GeoLines, Style, Geo, Bar, Line, Scatter3D, Line3D
import os
from concurrent.futures import ThreadPoolExecutor

class FlightTime:
    def __init__(self):
        self.to_city = ''
        self.date = []

    def getToCity(self):
        return self.to_city
    def getDate(self):
        return self.date

    def setToCity(self, city):
        self.to_city = city
    def setDate(self, date):
        self.date = date


class PlaneTime:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
        self.from_city_code = ''
        self.cities_code = {}
        self.flight_tag= ''
        self.url_list = []
        self.flight_time_list = []
        self.total_link = 0 # 目标城市的数目
        self.local = 'static/html'


        # 初始化一些函数
        self.setMapType()
        self.setCitiesCodes()

    # 输入检查
    def checkFromCity(self, from_city):
        self.from_city = from_city
        # 1、检查输入的城市是否有飞机场
        if self.from_city in self.cities_code:
            # 2、检查输入城市是否能在地图上标识
            try:
                plane_map = GeoLines("航线分时展示", **self.style.init_style)
                plane_map.add('', [[from_city, '大连']],tooltip_formatter="{a} : {c}", **self.style_geo)
            except Exception as e:
                print('抱歉，输入城市无法显示，你可以尝试输入其他城市。')
                return False

            self.from_city_code = self.cities_code[self.from_city]
            if not os.path.exists(self.local):
                os.makedirs(self.local)
            print('初始化链接。。。')

            return True
        else:
            print('起点城市名输入错误,请重新输入')
            return False

    # 设置城市编码
    def setCitiesCodes(self):
        self.cities_code = {
            "YIE": "阿尔山", "AKU": "阿克苏", "RHT": "阿拉善右旗", "AXF": "阿拉善左旗", "AAT": "阿勒泰", "NGQ": "阿里", "MFM": "澳门"
            , "AQG": "安庆", "AVA": "安顺", "AOG": "鞍山", "RLK": "巴彦淖尔", "AEB": "百色", "BAV": "包头", "BSD": "保山", "BHY": "北海",
                "BJS": "北京"
            , "DBC": "白城", "NBS": "白山", "BFJ": "毕节", "BPL": "博乐", "CKG": "重庆", "BPX": "昌都", "CGD": "常德", "CZX": "常州"
            , "CHG": "朝阳", "CTU": "成都", "JUH": "池州", "CIF": "赤峰", "SWA": "潮州", "CGQ": "长春", "CSX": "长沙", "CIH": "长治",
                "CDE": "承德"
            , "CWJ": "沧源", "DAX": "达州", "DLU": "大理", "DLC": "大连", "DQA": "大庆", "DAT": "大同", "DDG": "丹东", "DCY": "稻城",
                "DOY": "东营"
            , "DNH": "敦煌", "DAX": "达县", "LUM": "德宏", "EJN": "额济纳旗", "DSN": "鄂尔多斯", "ENH": "恩施", "ERL": "二连浩特",
                "FUO": "佛山"
            , "FOC": "福州", "FYJ": "抚远", "FUG": "阜阳", "KOW": "赣州", "GOQ": "格尔木", "GYU": "固原", "GYS": "广元", "CAN": "广州",
                "KWE": "贵阳"
            , "KWL": "桂林", "HRB": "哈尔滨", "HMI": "哈密", "HAK": "海口", "HLD": "海拉尔", "HDG": "邯郸", "HZG": "汉中", "HGH": "杭州",
                "HFE": "合肥"
            , "HTN": "和田", "HEK": "黑河", "HET": "呼和浩特", "HIA": "淮安", "HJJ": "怀化", "TXN": "黄山", "HUZ": "惠州", "JXA": "鸡西",
                "TNA": "济南"
            , "JNG": "济宁", "JGD": "加格达奇", "JMU": "佳木斯", "JGN": "嘉峪关", "SWA": "揭阳", "JIC": "金昌", "KNH": "金门", "JNZ": "锦州"
            , "CYI": "嘉义", "JHG": "景洪", "JSJ": "建三江", "JJN": "晋江", "JGS": "井冈山", "JDZ": "景德镇", "JIU": "九江",
                "JZH": "九寨沟", "KHG": "喀什"
            , "KJH": "凯里", "KGT": "康定", "KRY": "克拉玛依", "KCA": "库车", "KRL": "库尔勒", "KMG": "昆明", "LXA": "拉萨", "LHW": "兰州",
                "HZH": "黎平"
            , "LJG": "丽江", "LLB": "荔波", "LYG": "连云港", "LPF": "六盘水", "LFQ": "临汾", "LZY": "林芝", "LNJ": "临沧", "LYI": "临沂",
                "LZH": "柳州"
            , "LZO": "泸州", "LYA": "洛阳", "LLV": "吕梁", "JMJ": "澜沧", "LCX": "龙岩", "NZH": "满洲里", "LUM": "芒市", "MXZ": "梅州",
                "MIG": "绵阳"
            , "OHE": "漠河", "MDG": "牡丹江", "MFK": "马祖", "KHN": "南昌", "NAO": "南充", "NKG": "南京", "NNG": "南宁", "NTG": "南通",
                "NNY": "南阳"
            , "NGB": "宁波", "NLH": "宁蒗", "PZI": "攀枝花", "SYM": "普洱", "NDG": "齐齐哈尔", "JIQ": "黔江", "IQM": "且末",
                "BPE": "秦皇岛", "TAO": "青岛"
            , "IQN": "庆阳", "JUZ": "衢州", "RKZ": "日喀则", "RIZ": "日照", "SYX": "三亚", "XMN": "厦门", "SHA": "上海", "SZX": "深圳",
                "HPG": "神农架"
            , "SHE": "沈阳", "SJW": "石家庄", "TCG": "塔城", "HYN": "台州", "TYN": "太原", "YTY": "泰州", "TVS": "唐山", "TCZ": "腾冲",
                "TSN": "天津"
            , "THQ": "天水", "TGO": "通辽", "TEN": "铜仁", "TLQ": "吐鲁番", "WXN": "万州", "WEH": "威海", "WEF": "潍坊", "WNZ": "温州",
                "WNH": "文山"
            , "WUA": "乌海", "HLH": "乌兰浩特", "URC": "乌鲁木齐", "WUX": "无锡", "WUZ": "梧州", "WUH": "武汉", "WUS": "武夷山",
                "SIA": "西安", "XIC": "西昌"
            , "XNN": "西宁", "JHG": "西双版纳", "XIL": "锡林浩特", "DIG": "香格里拉(迪庆)", "XFN": "襄阳", "ACX": "兴义", "XUZ": "徐州",
                "HKG": "香港"
            , "YNT": "烟台", "ENY": "延安", "YNJ": "延吉", "YNZ": "盐城", "YTY": "扬州", "LDS": "伊春", "YIN": "伊宁", "YBP": "宜宾",
                "YIH": "宜昌"
            , "YIC": "宜春", "YIW": "义乌", "INC": "银川", "LLF": "永州", "UYN": "榆林", "YUS": "玉树", "YCU": "运城", "ZHA": "湛江",
                "DYG": "张家界"
            , "ZQZ": "张家口", "YZY": "张掖", "ZAT": "昭通", "CGO": "郑州", "ZHY": "中卫", "HSN": "舟山", "ZUH": "珠海",
                "WMT": "遵义(茅台)", "ZYI": "遵义(新舟)"}
        # 翻转编号
        self.cities_code = dict([val, key] for key, val in self.cities_code.items())


    # 获得航班标签
    def getFlightTag(self):
        link = 'http://flights.ctrip.com/schedule/' + self.from_city_code + '..html'
        try:
            r = requests.get(link, headers=self.headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            # 匹配规则,获得所需信息
            self.flight_tag = soup.find_all('div', class_='m')
            return True
        except:
            print('网络环境较差请重试！')
            return False

    # 通过正则匹配获取信息
    def tagToList(self):
        # 正则匹配所有到达目标城市
        to_city_pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 匹配汉字方式
        # 匹配结果为 大连-北京 的样子
        to_city_list = to_city_pattern.findall(str(self.flight_tag))

        # 目标城市的子链接
        to_city_url_pattern = re.compile(r'\bhttp\S*?html\b')
        to_city_url_list = to_city_url_pattern.findall(str(self.flight_tag))

        # 统计一共需要爬取的目标城市的个数
        for i in range(0, len(to_city_list)):
            if to_city_list[i*2] != self.from_city:
                self.total_link = i
                break

        # 为到达城市的数据结构（类）添加数据,包括达到城市
        # 初始化线程池
        pool = ThreadPoolExecutor(self.total_link)

        for i in range(0, self.total_link):
            done = pool.submit(self.request, to_city_url_list[i], to_city_list[i*2 + 1])
            done.add_done_callback(self.getDepartureTimeList)
        pool.shutdown(wait=True)


    def request(self, url, to_city_name ):
        try:
            return (requests.get(url, headers=self.headers, timeout=10), to_city_name)
        except:
            pass
            #print('网络连接出错')

    # 从链接爬取航班开始时间
    def getDepartureTimeList(self, future):

        flight_time = FlightTime()
        try:
            r, name = future.result()
        except:
            return

        # 设置到达城市的名字
        flight_time.setToCity(name)
        departure_time_list = []

        soup = BeautifulSoup(r.text, 'html.parser')

        # html标签树匹配规则
        flight_time_html = soup.find_all('td', align='right')
        # 正则匹配规则
        pattern = re.compile(r'\d{1,2}:\d{1,2}')  # 匹配时间
        departure_time_list = pattern.findall(str(flight_time_html))

        # 检查是否有扩展链接
        new_page = soup.find_all('div', class_='schedule_page_list clearfix')
        if len(new_page) != 0:
            try:
                url_pattern = re.compile(r'\bhttp\S*?html\b')
                other_url_list = url_pattern.findall(str(new_page))

                for i in range(1, len(other_url_list)):
                    other_r = requests.get(other_url_list[i], headers=self.headers, timeout=10)
                    other_soup = BeautifulSoup(other_r.text, 'html.parser')
                    other_flight_time_html = other_soup.find_all('td', align='right')
                    departure_time_list.extend(pattern.findall(str(other_flight_time_html)))
            except Exception as e:
                pass


        # 设置到达时间的列表
        flight_time.setDate(departure_time_list)
        # 每个到达城市类组成一个集合
        self.flight_time_list.append(flight_time)


    # 将 城市-时间 的数据结构转化为 时间-城市
    def sortTime(self):
        self.flight_data = [set() for i in range(24)]  # 借助集合排除重复名字
        for item in self.flight_time_list:
            for date in item.getDate():
                self.flight_data[int(date[0:2])].add(item.getToCity())

    # 将列表的数据转化为 html文件
    def setMapType(self):
        self.style = Style(
            page_title='分时航线图',
            title_top="#fff",
            title_pos="center",
            title_color='red',
            width=1000,
            height=800,
            background_color="#404a59"  # 背景设为灰色
        )
        self.style_geo = self.style.add(
            is_label_show=True,         # 标签的有无
            line_curve=0.2,             # 曲线的弯曲度
            line_opacity=0.5,           # 航线的透明度
            legend_text_color="#eee",
            legend_pos="right",         # 示例的位置
            geo_effect_symbol="plane",
            geo_effect_symbolsize=15,   # 飞机大小
            label_color=['#ffa022', '#ffa022', '#46bee9'],
            label_pos="right",
            label_formatter="{b}",      # 地方标签的格式
            label_text_color="#eee",
        )

    # 读取数据并在地图上绘制
    def drawRoute(self):
        for i in range(len(self.flight_data)):
            html_data = []
            if len(self.flight_data[i]) != 0:
                self.renderHtml(i, html_data)
            else:
                self.NoneHtml(i)

    # 必须用一个新的方法防止在同一张图上叠加生成
    def renderHtml(self, leave_time, html_data):
        plane_map = GeoLines("航线分时展示", **self.style.init_style)  # 相当于设置背景

        for city_name in self.flight_data[leave_time]:

            html_data.append([self.from_city, city_name])
            map_name = '在' + str(leave_time) + '时从' + self.from_city + '起飞的飞机:'
            try:
                plane_map.add(map_name, html_data,
                                   tooltip_formatter="{a} : {c}", **self.style_geo)
            except Exception as e:
                pass  # 忽略无法标识出来的城市

        plane_map.render(self.local + '/t' + str(leave_time+1) + '.html')

    def NoneHtml(self, leave_time):

        map_name = '在' + str(leave_time) + '时从' + self.from_city + '起飞的飞机:0'
        plane_map = Geo(map_name, **self.style.init_style)  # 相当于设置背景

        html_data_temp = [self.from_city]
        data_temp = [0]


        plane_map.add('',html_data_temp, data_temp,
                     is_visualmap=True, is_label_show=True)

        plane_map.render(self.local + '/t' + str(leave_time + 1) + '.html')


    def blackHtml(self, ):
        pass


    # 控制函数
    def getRouteHTML(self):
        if plane.getFlightTag():
            plane.tagToList()
            plane.sortTime()
            plane.drawRoute()
            return True
        else:
            return False


plane=PlaneTime()

# Flask
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query',methods=['GET','POST'])
def query():
    if request.method=="POST":
        from_city=request.form['station']
        print(from_city)
        while (True):
            if plane.checkFromCity(from_city):
                break
            else:
                message = 'input error'
                print('输入有错')
                return render_template('index.html', message=message)

        if plane.getRouteHTML():
            print(from_city)
            # start(from_city)
            # return "from query"
            return render_template('index.html')
        else:
            print('error')
            return render_template('index.html',message='网络环境较差请重试')

    # return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)