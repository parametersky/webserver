#coding=utf-8
from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant,MenuItem

app=Flask(__name__)
app.debug = True
app.secret_key="123321"
toolbar = DebugToolbarExtension(app)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
@app.route('/restaurant')
def HelloWorld():
    srestaurant = session.query(Restaurant).all()
    items = session.query(Restaurant).all()
    result = ''
    for item in items:
        result += '<a href="/restaurant/%d">%s</a>' % (item.id,item.name)
        result += '</br>'
        result += '</br>'
    return result
@app.route('/restaurant/JSON/')
def restaurantJSON():
    srestaurant = session.query(Restaurant).all()
    content = [i.serialize for i in srestaurant]
    #return value as unicode string, not chinese character
    return jsonify(Restaurants=[i.serialize for i in srestaurant],JSON_AS_ASCII=False,encoding='utf-8')
    #return value as chinese
    # result = "{'name':'水煮牛肉'}"
    # return json.dumps(result,ensure_ascii=False)

@app.route('/restaurant/<int:resid>/')
def ShowMenu(resid):
    srestaurant = session.query(Restaurant).filter_by(id=resid).one()
    print srestaurant.name
    result = ''
    items = session.query(MenuItem).filter_by(restaurant=srestaurant).all()
    if items:
        return render_template('menu.html',restaurant=srestaurant,items=items)
#        for item in items:
#            result += item.name
#            result += '</br>'
#        return result
    return "Sorry"
@app.route('/restaurant/<int:resid>/createMenuItem',methods=['POST','GET'])
def CreateMenuItem(resid):
    print request.method
    sRes = session.query(Restaurant).filter_by(id=resid).one()
    if request.method == 'POST':
        if request.form['menu_name']:
            print request.form['menu_name']
            menu = MenuItem(name=request.form['menu_name'],restaurant = sRes)
            session.add(menu)
            session.commit()
            return redirect(url_for('ShowMenu',resid=resid))
    else:
        print "dispose task %s" % request.method
        return render_template('createMenuItem.html',restaurant=sRes)
        


@app.route('/restaurant/<int:resid>/<int:menuid>/detele/')
def Delete(resid,menuid):
    sRes = session.query(Restaurant).filter_by(id=resid).one()
    menu = session.query(MenuItem).filter_by(id=menuid).filter_by(restaurant=sRes).one()
    if menu:
        session.delete(menu)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('ShowMenu',resid=resid))
    return "Sorry"
@app.route('/restaurant/<int:resid>/<int:menuid>/edit/',methods=['GET','POST'])
def Edit(resid,menuid):
    sRes = session.query(Restaurant).filter_by(id=resid).one()
    menu = session.query(MenuItem).filter_by(id=menuid).filter_by(restaurant=sRes).one()
    if not menu:
        return "Error"
    if request.method == 'POST':
        if request.form['menu_name']:
            menu.name = request.form['menu_name']#.decode('utf-8')
        else:
            return "Sorry"
        session.add(menu)
        session.commit()
        return redirect(url_for('ShowMenu',resid=sRes.id))
    else:
        return render_template('editMenuItem.html',restaurant=sRes,menuitem=menu)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
