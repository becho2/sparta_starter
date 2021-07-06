import requests
from bs4 import BeautifulSoup
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
@app.route('/memo', methods=['POST'])
def write_review():
    url_rec = request.form['url']
    comment_rec = request.form['comment']
    # print(url_rec, comment_rec)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_rec, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1)
    # tr = soup.select_one('#body-content > div.newest-list > div > table > tbody > tr')
    # content > div.article > div.mv_info_area > div.poster > a > img
    title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
    image_url = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')['src']
    synopsis = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > p').text
    print(title, image_url, synopsis)

    doc = {
        "url": url_rec,
        "comment": comment_rec,
        "title": title,
        "imageUrl": image_url,
        "synopsis": synopsis
    }
    res = db.alonememo.insert_one(doc)
    print(res)
    return jsonify({'msg': '등록 완료!'})


@app.route('/memo', methods=['GET'])
def read_reviews():
    # sample_receive = request.args.get('sample_give')
    memos = list(db.alonememo.find({}, {'_id': False}))
    return jsonify({'msg': '성공!','memos': memos})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)