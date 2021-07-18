from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbhomework
## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')
# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_receive = request.form['name_give']
    cnumber_receive = request.form['cnumber_give']
    address_receive = request.form['address_give']
    pnumber_receive = request.form['pnumber_give']
    doc = {
        'name': name_receive,
        'cnumber': cnumber_receive,
        'address': address_receive,
        'pnumber': pnumber_receive
    }
    db.orders.insert_one(doc)
    return jsonify({'msg':'주문 완료!'})
# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': '이 요청은 GET!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)