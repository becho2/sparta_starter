from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
col = db.movies

# 3. 매트릭스 평점 0 만들기
col.update_one({'title':'매트릭스'},{"$set":{'point':"0" }})

# 1. 매트릭스 평점 가져오기
matrix = col.find_one({'title':'매트릭스'},{'_id':False})
print('매트릭스의 평점은?')
print(matrix['point'])

# 2. 매트릭스 평점과 같은 영화제목들 가져오기
print('이와 같은 평점의 영화들은 무엇?')
# qry = {"$and":[{'point': matrix['point']},{'title':{"$not":'매트릭스'}}]}
qry = {'point': matrix['point'] }
other_movies = list(col.find(qry))
#
# print(other_movies)
for movie in other_movies:
    print(movie['title'])