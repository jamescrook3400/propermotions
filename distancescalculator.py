from astrodbkit.astrodbkit import astrodb
db = astrodb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')
data=db.query('select parallax,id from parallaxes')
distancelist=[]
for num,ids in data:
            distance= 1.0 / (num), ids
            distancelist.append(distance)

names=db.query('select source_id from parallaxes')
