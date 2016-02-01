from BDNYCdb import BDdb
import numpy as np
import RADEC 
db=BDdb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')

#ADD COMMENTS and generate shortnames and update that way
#run g
old=np.genfromtxt('/Users/jamescrook/Documents/Modules/faherty08.txt', delimiter='|', dtype=object)
new=np.genfromtxt('/Users/jamescrook/Documents/Modules/fahertydata.txt', delimiter=',', dtype=object)
newpublications=[[25,208],[50,212],[49,213],[53,214],[59,215],[342,217],[94,221],[110,223],[334,224],[118,225],["NULL",209],["NULL", 210],["NULL",216],["NULL",218],["NULL",219],["NULL",222],["NULL",227],["NULL", 229],[193,231],[168,232],[193,233],[300,234],[346,235],[514,228],[360,206],[396,205],[463, 204],["NULL",202],["NULL",247],["NULL",246],["NULL",245],[467,241],["NULL",238],[228,236],[244,237],[257,242],[263,244],[259,243],[255,240], [166,230]]
DB_data=db.dict("select * from sources").fetchall()
global new, old
def generate_sourceid(data):  
    allids=[]
    
    #For objects without shortnames
    for (name) in data:
        shortname = RADEC.get_shortname(name)
        if shortname != '':
            try:
                ida=db.query("select id from sources where shortname='{}'".format(shortname))[0]
                allids.append(ida)
            except:
                ida=''
                allids.append(ida)
        else:
            ida=''
            allids.append(ida)

    return allids
    print data
    
#adds new faherty data
def add_new_data(new):
    db.add_data('/Users/jamescrook/Documents/Modules/fahertydata.txt', 'proper_motions', delimiter = ',', multiband=False)
    
#adds old faherty data
def add_old_data(old):
    db.add_data('/Users/jamescrook/Documents/Modules/faherty08.txt', 'proper_motions', delimiter='|', multiband=False)

#updates publication IDs
#FOR SOME REASON THIS ISNT UPDATING STUFF?
def update_publications(newpublications):
    for old,new in newpublications: db.modify("update proper_motions set publication_id={} where publication_id={}".format(new,old))
