from astrodbkit.astrodbkit import astrodb
import numpy as np
import RADEC 
db=astrodb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')

#ADD COMMENTS and generate shortnames and update that way
newpublications=[[25,208],[50,212],[49,213],[53,214],[59,215],[342,217],[94,221],[110,223],[334,224],[118,225],[591,209],[590, 210],['',216],['',218],[290,219],[592,222],['',227],['', 229],[193,231],[168,232],[193,233],[300,234],[346,235],[514,228],[360,206],[396,205],[463, 204],['',202],['',247],['',246],['',245],[467,241],['',238],[228,236],[244,237],[257,242],[263,244],[259,243],[255,240], [166,230]]
DB_data=db.query("select * from sources", fmt='dict')
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
def add_new_data():
    db.add_data('new.txt', 'proper_motions', delimiter=',')
    
#adds old faherty data
def add_old_data():
    db.add_data('old.txt', 'proper_motions', delimiter='|')

#updates publication IDs
#FOR SOME REASON THIS ISNT UPDATING STUFF?
def update_publications(newpublications):
    for new,old in newpublications:
      if new and old: db.modify("update proper_motions set publication_id={} where publication_id={}".format(new,old))
      else: db.modify("update proper_motions set publication_id=NULL where publication_id={}".format(old))
