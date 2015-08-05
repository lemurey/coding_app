from flask import Flask 
from flask import (request,
                   redirect,
                   url_for,
                   g,
                   session,
                   render_template
                  )

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session



import os
import csv

# from rq import Queue
# from rq.job import Job 
# from worker import conn

from uuid import uuid1

from numpy.random import randint,random,choice

from random import sample

from collections import Counter

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# q = Queue(connection=conn)

from database import db_session
from models import Users, Codes, RaterCodes, Raters, Urls


def get_user():
    try:
        user = session['user']
    except KeyError:
        print 'creating new user'
        session['user'] = str(uuid1())
        add_user(session['user'])
        user = session['user']
        session['user_urls'] = Counter()
        session['num_rated'] = len(session['user_urls'])
        session['possible'] = get_possible()
        session.permanent = True
    return None

def add_user(uid):
    new_rater = Raters(id=uid)
    db_session.add(new_rater)
    db_session.commit()

def initial_photos():
    photos = ['https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11325840_464867873683085_649034298_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11378012_1446069692376360_1541980031_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfp1/t51.2885-15/e15/10802478_725003310882291_422501228_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xap1/t51.2885-15/e15/11205645_942559225796075_1397163383_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfp1/t51.2885-15/e15/11005230_1600894226796218_423884455_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfp1/t51.2885-15/e15/10990615_339024099639805_1506985481_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11337172_1601345906784701_792942460_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xpf1/t51.2885-15/e15/10431970_1527617597452635_1251699668_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xpa1/t51.2885-15/e15/10832030_1542303966015579_505985177_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11252880_424152497759635_1687528232_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11357918_1570231713252979_2046681392_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11358041_994020273965005_67598926_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11230394_1584053608503462_1190894731_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xpa1/t51.2885-15/e15/11116874_1479321492357933_386092792_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11244438_994229953928484_1016182571_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfp1/t51.2885-15/e15/11007813_756773111098510_1078743960_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xap1/t51.2885-15/e15/11190144_1445677955726198_995507436_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/s640x640/sh0.08/e35/11333300_1006787476006608_646716080_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/s640x640/sh0.08/e35/11377400_773128459471146_879048613_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11376056_792393374190837_75061903_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11374683_1462559684040803_114285998_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11272956_824340250993620_931029359_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xpa1/t51.2885-15/e15/1962890_1634834076744393_432924718_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xpa1/t51.2885-15/e15/11190877_946815485362618_1777865940_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/e15/11333741_874816455887108_2022391728_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xfp1/t51.2885-15/e15/10369471_1417185468555459_1668616953_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xap1/t51.2885-15/e15/11190334_688792467933804_866058668_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xap1/t51.2885-15/e15/10785057_1578240325739866_649231870_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xtf1/t51.2885-15/e15/11123653_1716414691918980_2110101112_n.jpg',
              'https://scontent.cdninstagram.com/hphotos-xaf1/t51.2885-15/e15/11358240_1617051675202220_2068834932_n.jpg']
    # with open('inital.csv','rb') as f:
    #     test = csv.reader(f,delimiter='\n')
    #     for row in test:
    #         photos.append(row[0])
    return photos

def get_random_entries():
    query = db_session.query(Urls.id,Urls.url_high)
    test = choice(xrange(251577,515579),size = 1,replace=False)
    possible = []
    for element in test:
        one = query.filter_by(id = element).first()
        if one:
            possible.append(one)
        else:
            get_random_entries()
    return filter_queries(possible)

def filter_queries(results):
    p_ids = []
    p_urls = []
    for entry in results:
        p_ids.append(entry[0])
        p_urls.append(entry[1])
    return (p_ids,p_urls)

def get_possible():
    query = db_session.query(Urls.id,Urls.url_high)
    poss_list = initial_photos()
    possible = query.filter(Urls.url_high.in_(poss_list)).all()
    return filter_queries(possible)

def get_images():
    get_image = True
    iterations = 0
    num_rated = session.get('num_rated')
    print 'number rated already is: ',num_rated
    if num_rated < 30:
        pos_images = session.get('possible')
    else:
        pos_images = get_random_entries()
    while get_image:
        iterations += 1
        if iterations > 500:
            print 'Getting new set of images cause it keeps searching'
            pos_images = get_random_entries()
        while len(pos_images) == 0:
            pos_images = get_random_entries()
        index = randint(len(pos_images[0]))
        cur_id = pos_images[0][index]
        cur_image = pos_images[1][index]
        check = unicode(cur_id)
        if check not in session.get('user_urls').keys():
            get_image = False
    return cur_id,cur_image
            

def update_db(label,post_id):
    pass
    #return id_key,label
    
@app.route('/')
def welcome():
    if 'user' not in session.keys():
        # job = q.enqueue_call(
        #     func=get_user(),args=None,result_ttl=5000)
        # print (job.get_id())
        get_user()
    return redirect(url_for('images'))

@app.route('/image')
def images():
    if 'user' not in session.keys():
        print 'pushing you to welcome'
        return redirect(url_for('welcome'))
    index,image = get_images()
    s = session.get('user')
    index = str(index) +''.join(sample(s,len(s)))
    return render_template('image.html',data = (image,index))

@app.route('/<num_id>/yes',methods=['GET'])
def is_tattoo(num_id):
    #image_id, label = update_db('yes',post_id)
    image_id = int(num_id[:-36])
    return redirect(url_for('write_database',image_id = image_id,
                                             image_code = 'yes'))

@app.route('/<num_id>/no',methods=['GET'])
def not_tattoo(num_id):
    #image_id, label = update_db('no',post_id)
    image_id = int(num_id[:-36])
    return redirect(url_for('write_database',image_id = image_id,
                                             image_code = 'no'))

@app.route('/<num_id>/maybe',methods=['GET'])
def maybe_tattoo(num_id):
    #image_id, label = update_db('maybe',post_id)
    image_id = int(num_id[:-36])
    return redirect(url_for('write_database',image_id = image_id,
                                             image_code = 'maybe'))

@app.route('/<image_id>/<image_code>/db_write')
def write_database(image_id,image_code):
    e = None
    output = RaterCodes(url_id = image_id, 
                        rater_id = session.get('user'),
                        code = image_code)
    try:
        db_session.add(output)
        db_session.commit()
    except Exception as e:
        print 'exception was: ',e
        print 'database commit error'
    else:
        print 'successfully commited'
        session['num_rated'] += 1
        session['user_urls'][image_id] = 1
    return redirect(url_for('images'))




@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)