from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

import re
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbseamovies

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&date=20210726', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#old_content > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.title > div > a')

    if a_tag is not None:
        # title name
        title = a_tag.text

        # page url
        url = 'https://movie.naver.com' + a_tag['href']

        data2 = requests.get(url, headers=headers)
        soup2 = BeautifulSoup(data2.text, 'html.parser')
        overall = soup2.select_one('#content > div.article > div.wide_info_area')

        # poster
        og_image = soup2.select_one('meta[property="og:image"]')['content']

        # star
        star = '개봉예정'
        if overall.select_one('#pointNetizenPersentWide') is not None:
            star = overall.select_one('#pointNetizenPersentWide').text

        # released date
        released = '미정'
        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)') is not None:
            released = overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)').text

        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)') is not None:
            released += overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)').text

        # genre
        total_genre = overall.select_one('div.mv_info > p > span:nth-child(1)')
        genre1 = total_genre.select_one('a:nth-child(1)').text
        genre2 = ''
        genre3 = ''
        genre3 = ''
        genre4 = ''

        if total_genre.select_one('a:nth-child(2)') is not None:
            genre2 = ', ' + total_genre.select_one('a:nth-child(2)').text

        if total_genre.select_one('a:nth-child(3)') is not None:
            genre3 = ', ' + total_genre.select_one('a:nth-child(3)').text

        if total_genre.select_one('a:nth-child(4)') is not None:
            genre4 = ', ' + total_genre.select_one('a:nth-child(4)').text

        genre = genre1 + genre2 + genre3 + genre4

        # director
        director = overall.select_one('div.mv_info > div.info_spec2 > dl.step1 > dd > a').text
#
        # actors
        total_actors = overall.select_one('div.mv_info > div.info_spec2 > dl.step2 > dd')
        actor1 = '미정'
        actor2 = ''
        actor3 = ''

        if total_actors is not None:
            if total_actors.select_one('a:nth-child(1)') is not None:
                actor1 = total_actors.select_one('a:nth-child(1)').text

            if total_actors.select_one('a:nth-child(2)') is not None:
                actor2 = ', ' + total_actors.select_one('a:nth-child(2)').text

            if total_actors.select_one('a:nth-child(3)') is not None:
                actor3 = ', ' + total_actors.select_one('a:nth-child(3)').text

        actor = actor1 + actor2 + actor3

        # synopsis
        try:
            summary = soup2.find('div', {'class': 'story_area'}).find('p', {'class': 'con_tx'})
            summary = re.sub('[^\da-zA-Z가-힣/. ]', '', summary.text).strip()
        except:
            summary = ''

        doc = {
            'title': title,
            'pageurl': url,
            'ogimage': og_image,
            'star': star,
            'released': released,
            'genre': genre,
            'director': director,
            'actors': actor,
            'synopsis': summary,
            'like': 0
        }
        db.view.insert_one(doc)

data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210726', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#old_content > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.title > div > a')

    if a_tag is not None:
        # title name
        title = a_tag.text

        # page url
        url = 'https://movie.naver.com' + a_tag['href']

        data2 = requests.get(url, headers=headers)
        soup2 = BeautifulSoup(data2.text, 'html.parser')
        overall = soup2.select_one('#content > div.article > div.wide_info_area')

        # poster
        og_image = soup2.select_one('meta[property="og:image"]')['content']

        # star
        star = '개봉예정'
        if overall.select_one('#pointNetizenPersentWide') is not None:
            star = overall.select_one('#pointNetizenPersentWide').text

        # released date
        released = '미정'
        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)') is not None:
            released = overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)').text

        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)') is not None:
            released += overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)').text

        # genre
        total_genre = overall.select_one('div.mv_info > p > span:nth-child(1)')
        genre1 = total_genre.select_one('a:nth-child(1)').text
        genre2 = ''
        genre3 = ''
        genre3 = ''
        genre4 = ''

        if total_genre.select_one('a:nth-child(2)') is not None:
            genre2 = ', ' + total_genre.select_one('a:nth-child(2)').text

        if total_genre.select_one('a:nth-child(3)') is not None:
            genre3 = ', ' + total_genre.select_one('a:nth-child(3)').text

        if total_genre.select_one('a:nth-child(4)') is not None:
            genre4 = ', ' + total_genre.select_one('a:nth-child(4)').text

        genre = genre1 + genre2 + genre3 + genre4

        # director
        director = '미정'
        if overall.select_one('div.mv_info > div.info_spec2 > dl.step1 > dd > a') is not None:
            director = overall.select_one('div.mv_info > div.info_spec2 > dl.step1 > dd > a').text

        # actors
        total_actors = overall.select_one('div.mv_info > div.info_spec2 > dl.step2 > dd')
        actor1 = '미정'
        actor2 = ''
        actor3 = ''

        if total_actors is not None:
            if total_actors.select_one('a:nth-child(1)') is not None:
                actor1 = total_actors.select_one('a:nth-child(1)').text

            if total_actors.select_one('a:nth-child(2)') is not None:
                actor2 = ', ' + total_actors.select_one('a:nth-child(2)').text

            if total_actors.select_one('a:nth-child(3)') is not None:
                actor3 = ', ' + total_actors.select_one('a:nth-child(3)').text

        actor = actor1 + actor2 + actor3

        # synopsis
        try:
            summary = soup2.find('div', {'class': 'story_area'}).find('p', {'class': 'con_tx'})
            summary = re.sub('[^\da-zA-Z가-힣/. ]', '', summary.text).strip()
        except:
            summary = ''

        doc = {
            'title': title,
            'pageurl': url,
            'ogimage': og_image,
            'star': star,
            'released': released,
            'genre': genre,
            'director': director,
            'actors': actor,
            'synopsis': summary,
            'like': 0
        }
        db.star.insert_one(doc)

data = requests.get('https://movie.naver.com/movie/running/current.naver', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

for tr in trs:
    a_tag = tr.select_one('dl > dt > a')

    if a_tag is not None:
        # title name
        title = a_tag.text

        # page url
        url = 'https://movie.naver.com' + a_tag['href']

        data2 = requests.get(url, headers=headers)
        soup2 = BeautifulSoup(data2.text, 'html.parser')
        overall = soup2.select_one('#content > div.article > div.wide_info_area')

        # poster
        og_image = soup2.select_one('meta[property="og:image"]')['content']

        # star
        star = '개봉예정'
        if overall.select_one('#pointNetizenPersentWide') is not None:
            star = overall.select_one('#pointNetizenPersentWide').text

        # released date
        released = '미정'
        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)') is not None:
            released = overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(1)').text

        if overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)') is not None:
            released += overall.select_one('div.mv_info > p > span:nth-child(4) > a:nth-child(2)').text

        # genre
        total_genre = overall.select_one('div.mv_info > p > span:nth-child(1)')
        genre1 = total_genre.select_one('a:nth-child(1)').text
        genre2 = ''
        genre3 = ''
        genre3 = ''
        genre4 = ''

        if total_genre.select_one('a:nth-child(2)') is not None:
            genre2 = ', ' + total_genre.select_one('a:nth-child(2)').text

        if total_genre.select_one('a:nth-child(3)') is not None:
            genre3 = ', ' + total_genre.select_one('a:nth-child(3)').text

        if total_genre.select_one('a:nth-child(4)') is not None:
            genre4 = ', ' + total_genre.select_one('a:nth-child(4)').text

        genre = genre1 + genre2 + genre3 + genre4

        # director
        director = '미정'
        if overall.select_one('div.mv_info > div.info_spec2 > dl.step1 > dd > a') is not None:
            director = overall.select_one('div.mv_info > div.info_spec2 > dl.step1 > dd > a').text

        # actors
        total_actors = overall.select_one('div.mv_info > div.info_spec2 > dl.step2 > dd')
        actor1 = '미정'
        actor2 = ''
        actor3 = ''

        if total_actors is not None:
            if total_actors.select_one('a:nth-child(1)') is not None:
                actor1 = total_actors.select_one('a:nth-child(1)').text

            if total_actors.select_one('a:nth-child(2)') is not None:
                actor2 = ', ' + total_actors.select_one('a:nth-child(2)').text

            if total_actors.select_one('a:nth-child(3)') is not None:
                actor3 = ', ' + total_actors.select_one('a:nth-child(3)').text

        actor = actor1 + actor2 + actor3

        # synopsis
        try:
            summary = soup2.find('div', {'class': 'story_area'}).find('p', {'class': 'con_tx'})
            summary = re.sub('[^\da-zA-Z가-힣/. ]', '', summary.text).strip()
        except:
            summary = ''

        doc = {
            'title': title,
            'pageurl': url,
            'ogimage': og_image,
            'star': star,
            'released': released,
            'genre': genre,
            'director': director,
            'actors': actor,
            'synopsis': summary,
            'like': 0
        }
        db.current.insert_one(doc)


## HTML을 주는 부분
@app.route('/')
def home():
    # viewstar.py는 크롤링 작업을 하고 data는 robo로
    # viewstar.py를 import해서 시작전에 돌리고 시작
    return render_template('index.html')


@app.route('/view', methods=['GET'])
def most_viewed():
    most_viewed = list(db.view.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'fifty_viewed': most_viewed})


@app.route('/star', methods=['GET'])
def high_starred():
    highest_star = list(db.star.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'fifty_star': highest_star})


# API 역할을 하는 부분
@app.route('/love', methods=['GET'])
def most_loved():
    sorted = love()

    return jsonify({'sorted_like': sorted})


def love():
    all = list(db.view.find({}, {'_id': False}))
    star = list(db.star.find({}, {'_id': False}))
    current = list(db.current.find({}, {'_id': False}))

    for i in star:
        for j in all:
            if (j['title'] == i['title']):
                break
        else:
            all.append(i)

    for i in current:
        for j in all:
            if (j['title'] == i['title']):
                break
        else:
            all.append(i)

    # put movies in order of likes (0 -> higher number)
    all.sort(key=lambda m: m['like'])
    # reverse the list
    all.reverse()
    return all


@app.route('/movie')
def movie():
    title = request.args.get('title')
    # onemovie.py는 movie.html에 들어가야 할 data를 크롤링 하고 robo로 옮기는 python file
    # onemovie.py를 돌려서,특정한 영화 데이타를 db로 옮기고 밑에 있는 문장으로 data를 끌어온다(viewprac말고 다른데로)
    info = db.view.find_one({'title': title}, {'_id': False})

    if info is None:
        info = db.star.find_one({'title': title}, {'_id': False})

    if info is None:
        info = db.current.find_one({'title': title}, {'_id': False})


    return render_template('movie.html',
                           title=title,
                           pageurl=info['pageurl'],
                           image=info['ogimage'],
                           star=info['star'],
                           released=info['released'],
                           genre=info['genre'],
                           director=info['director'],
                           actors=info['actors'],
                           synopsis=info['synopsis'],
                           like=info['like'],
                           )


@app.route('/list')
def passing_list():
    title = request.args.get('type')

    return render_template('toplist.html',
                           title=title)


@app.route('/listing')
def type_list():
    type = request.args.get('type')

    if (type=='조회순'):
        some_list = list(db.view.find({}, {'_id': False}))

    if(type=='평점순'):
        some_list = list(db.star.find({}, {'_id': False}))

    if(type=='상영/예정작'):
        some_list = list(db.current.find({}, {'_id': False}))

    if(type=='좋아요순'):
        some_list = love()

    return jsonify({'result': 'success', 'fifty_list': some_list})


## API 역할을 하는 부분
@app.route('/search', methods=['POST', 'GET'])
def saving_search():
    if request.method == 'POST':
        searched_title = request.form['search-input']
        return redirect(url_for("moving_search", searchedmovie=searched_title))
    else:
        return render_template('search.html')


## HTML을 주는 부분
@app.route('/<searchedmovie>')
def moving_search(searchedmovie):
    info = db.view.find_one({'title': searchedmovie}, {'_id': False})

    if info is None:
        info = db.star.find_one({'title': searchedmovie}, {'_id': False})

    if info is None:
        info = db.current.find_one({'title': searchedmovie}, {'_id': False})

    if info is None:
        return render_template('search.html',
                               title=searchedmovie
                               )


    return render_template('search.html',
                           title=searchedmovie,
                           image=info['ogimage']
                           )


@app.route('/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']

    target_star = db.view.find_one({'title': name_receive}, {'_id': False})
    if target_star is not None:
        current_like = target_star['like']
        new_like = current_like + 1
        db.view.update_one({'title': name_receive}, {'$set': {'like': new_like}})

    if target_star is None:
        target_star = db.star.find_one({'title': name_receive}, {'_id': False})
        if target_star is not None:
            current_like = target_star['like']
            new_like = current_like + 1
            db.star.update_one({'title': name_receive}, {'$set': {'like': new_like}})

    if target_star is None:
        target_star = db.current.find_one({'title': name_receive}, {'_id': False})
        if target_star is not None:
            current_like = target_star['like']
            new_like = current_like + 1
            db.current.update_one({'title': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 눌렀습니다!'})


## API 역할을 하는 부분
@app.route('/comment', methods=['POST'])
def write_comment():
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    doc = {
        'title': name_receive,
        'comment': comment_receive
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '코맨트 저장 완료!'})


@app.route('/comment', methods=['GET'])
def read_reviews():
    title = request.args.get('title')

    comments = list(db.comment.find({'title': title}, {'_id': False}))

    return jsonify({'all_comments': comments})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


