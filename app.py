from flask import Flask, render_template, request, jsonify

import googlemaps
import time
import secrets

#創建Flask物件app并初始化
app = Flask(__name__)

#通過python裝飾器的方法定義路由地址
@app.route("/")
#定義方法 **用jinjia2引擎來渲染頁面**，并回傳一個index.html頁面
def root():
    return render_template("index.html")

#app的路由地址"/submit"即為ajax中定義的url地址，采用POST、GET方法均可提交
@app.route("/submit",methods=["GET", "POST"])
#從這里定義具體的函式 回傳值均為json格式
def submit():
    #由于POST、GET獲取資料的方式不同，需要使用if陳述句進行判斷
    if request.method == "POST":
        # 從前端拿數據
        name = request.form.get("name")
        age = request.form.get("age")
    if request.method == "GET":
        name = request.args.get("name")
        age = request.args.get("age")
    #如果獲取的資料為空
    if len(name) == 0 or len(age) == 0:
        # 回傳的形式為 json
        return {'message':"error!"}
    else:
        #將API憑證用以下指令包起來
        gmaps=googlemaps.Client(key="AIzaSyBSt6MtWDsAutL5HqJ0vOpuv_vgIf5Fm7o")

        #簡單的調用資料示範
        geocode_result = gmaps.geocode(name)

        #print(geocode_result)

        loc = geocode_result[0]['geometry']['location']
        rad = age

        results = []
        query_result = gmaps.places_nearby(keyword="餐廳",location=loc, radius=rad)
        results.extend(query_result['results'])
        while query_result.get('next_page_token'):
            time.sleep(2)
            query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
            results.extend(query_result['results'])    

        #用gmaps.places_radar這個代碼來查total有幾個結果
        #print("輔大為中心"+str(rad)+"公尺的餐廳數量: "+ str(len(results)))

        pids=[]
        for place in results:
            pids.append(place['place_id'])

        restaurant_info = []

        for id in pids:
            #print ("running")
            restaurant_info.append(gmaps.place(place_id=id, language='zh-TW')['result'])
            #每次間隔0.3sec
            #time.sleep(0.3)

        i = 0
        class food:
            def __init__(self, name, url):
                self.name = name
                self.url = url
        # creating list
        list = []
        for r in restaurant_info:
            restaurant_info[i] = r['name']
            # appending instances to list
            list.append(food(r['name'], r['url']))
            i = i + 1

        def selectsecrets(names):
            return secrets.choice(names)
        output = (selectsecrets(list))
        #print("The restaurant selected is: ", selectsecrets(restaurant_info))
        return {'message':"success!",'name':output.name,'age':output.url}
if __name__ == '__main__':
    #定義app在8080埠運行
    app.run(host="0.0.0.0",port=3000,debug=True)