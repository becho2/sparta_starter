from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    star_list = list(db.mystar.find({}, {'_id': False}).sort("like",-1))
    # print(star_list)
    return jsonify({'star_list': star_list})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_rec = request.form['name']
    like_now = db.mystar.find_one({'name': name_rec},{'_id': False})['like']
    like_plus = like_now + 1
    db.mystar.update_one({'name':name_rec},{'$set':{'like': like_plus}})
    return jsonify({'msg': '좋아요를 누르셨습니다!'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_rec = request.form['name']
    db.mystar.delete_one({'name':name_rec})
    return jsonify({'msg': '삭제되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)