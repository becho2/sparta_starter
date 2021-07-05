from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    title_rec = request.form['title']
    author_rec = request.form['author']
    review_rec = request.form['bookReview']
    doc = {"title": title_rec, "author": author_rec, "review": review_rec}
    res = db.reviews.insert_one(doc)
    print(res)
    return jsonify({'msg': '등록되었습니다. 좋은 리뷰 감사해요!'})


@app.route('/review', methods=['GET'])
def read_reviews():
    # sample_receive = request.args.get('sample_give')
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'msg': '성공!','reviews':reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)