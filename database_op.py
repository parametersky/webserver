#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant,MenuItem
import codecs
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


restaurantname = "data/restaurant.txt"
f = codecs.open(restaurantname,'r','utf-8') #use codesc to read file into utf-8
while True:
    line = f.readline().strip('\n')
    if line:
        xline = line#.decode('utf-8')
        res = Restaurant(name = xline)
        session.add(res)
    else:
        break
session.commit()
items = session.query(Restaurant).all()
for item in items:
    print item.name
print '\n'

def addMenuToRest(session,rest_name,menutext):
    rname = rest_name.decode('utf-8')
    restaurant_item = session.query(Restaurant).filter_by(name=rname).one()
    if not restaurant_item:
        print "cannot find item %s" % rest_name
        return
    try:
        fs = open(menutext,'r')
    except IOError:
        print "menu file cannot be opened"
        return

    while True:
        line = "".join(fs.readline().strip('\n').decode('utf-8').split())
        if line:
            menu = MenuItem(name=line,restaurant=restaurant_item,course="Main",description="delicious meal",price="25")
            session.add(menu)
        else:
            break;
    session.commit()

addMenuToRest(session,'四川菜馆','data/sichuancaiguan.txt')
addMenuToRest(session,'湖南菜馆','data/hunancaiguan.txt')
addMenuToRest(session,'上海菜馆','data/shanghaicaiguan.txt')
addMenuToRest(session,'广东菜馆','data/guangdongcaiguan.txt')
addMenuToRest(session,'江西菜馆','data/jiangxicaiguan.txt')

#rname = '四川菜馆'.decode('utf-8')
#chuancaiguan = session.query(Restaurant).filter_by(name=rname).one()
#if not chuancaiguan:
#    print "cannot find chuan cai guan"
#
#print "read menu"
#sichuancai = "data/sichuancaiguan.txt"
#fs = open(sichuancai,'r')
#while True:
#    line = fs.readline().strip('\n').decode('utf-8')
#    if line:
#        menu = MenuItem(name=line,restaurant=chuancaiguan)
#        session.add(menu)
#    else:
#        break;
#session.commit()

items = session.query(MenuItem).all()

for item in items:
    print item.name
print '\n'
#myfirstres = Restaurant(name = "Pizza Palace")
#session.add(myfirstres)
#session.commit()
#firstResult = session.query(Restaurant).first()

