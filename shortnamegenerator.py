from BDNYCdb import BDdb
import numpy as np
import re 
db=BDdb.get_db('/Users/jamescrook/Documents/Modules/BDNYC.db')
DB_data=db.list("select names,ra,dec from sources").fetchall()
#DA_data=np.genfromtxt('/Users/Joe/Desktop/obj_list.txt', delimiter=",", dtype=object)

#Function to generate shortnames from a given name for a list of objects
def get_shortname(name):
    #Establishes whether a given name has a "+" or a "-"  
    if "+" in name:
        n="+"
    else:
        n="-"
      
    #Splits up the name on a whitespace   
    com="ABab"
    nums="1234567890"
    q=re.split("\W+", name)
  
    #For the easiest names, where it is just "Survey J123456+78900"
    if len(q)==3:
        partone=q[1]
        parttwo=q[2]
      
        #Accounts for objects with names that have three parts seperated by a whitespace, but are not structured like "Survey J123456+78900"
        if partone[0]!="J":
            shortname = ''
            
          
        #Deals with objects that are structured properly 
        else:
            shortone=partone[1:5]
            if shortone[0] and shortone [1] and shortone [2] and shortone[3] in nums:
              
                #Deals with AB at the end
                if parttwo[-1] in com and parttwo[-2] in com: 
                    shorttwo=parttwo[:4]
                    shortname=shortone+n+shorttwo
                  
                #For companions     
                elif parttwo[-1] in com:
                    shorttwo=parttwo[:4]+parttwo[-1]
                    shortname= shortone+n+shorttwo
                  
                #For isolated objects
                else:
                    shorttwo=parttwo[:4]
                    shortname=shortone+n+shorttwo

            else:
                shortname = ''
              
    #For objects with a "." in their name, of which there were quite a few. It gives an object like "2MASS 123.4+567.8" the shortname "1234+5678"            
    if len(q)>3:  
        t=re.sub(r"\.",r"",name)
        o=re.split("\W+", t)
        p1=o[1]
        p2=o[2]
      
        #For objects like "Denis-P" that have an extra letter
        if len(p1)==1:
            partone=o[2]
            parttwo=o[3]
          
            #Gets rid of objects that don't start with "J"
            if partone[0]!="J":
                shortname = ''
                
        else:
            partone=p1
            parttwo=p2
            if partone[0]!="J":
                shortname = ''
                
        shortone=partone[1:5]
        if len(shortone)<4:
            shortname = ''
            
        elif shortone[0] and shortone [1] and shortone [2] and shortone[3] in nums:
            shortone=partone[1:5]
          
            #Deals with AB at the end
            if parttwo[-1] in com and parttwo[-2] in com: 
                shorttwo=parttwo[:4]
                shortname=shortone+n+shorttwo
              
            #Deals with companions
            elif parttwo[-1] in com:
                shorttwo=parttwo[:4]+parttwo[-1]
                shortname= shortone+n+shorttwo
              
            #Deals with isolated objects
            else:
                shorttwo=parttwo[:4]
                shortname=shortone+n+shorttwo
          
        else:
            shortname = ''         
          
    #Passes on objects with "q" values less than 3    
    if len(q)<3: 
        shortname = ''
    
    #Gets rid of any weird shortnames before priting
    for letter in shortname:
        if letter not in nums:
            if letter not in com:
                shortname = ''
    return shortname

def generate_DA_shortnames(DA_data):  
    allshortnames=[]
    allnames=[]
    wierdones=[]
    
    #For objects without shortnames
    for (name, ra, dec) in DA_data:
        shortname = get_shortname(name)
        allshortnames.append(shortname)
    
    data = np.concatenate([np.array([allshortnames]),DA_data.T]).T
    
    return data

def generate_DB_shortnames():
    """
    Generates shortnames for objects in need using designations and names    
    """
    need_sn = db.list("select id,names,designation from sources where shortname is null or shortname=''").fetchall()
    for source_id,names,designation in need_sn:
      shortname = ''
      if designation: shortname = get_shortname(designation)
      if names and not shortname: shortname = get_shortname(names)
      if shortname: 
        response = raw_input("Update source {} {} {} with shortname {}?[y,n] ".format(source_id,designation,names,shortname))
        if response=='y': db.list("update sources set shortname='{}' where id={}".format(shortname,source_id))
        else: print 'Not updated.'
    
def fix_RA(data):       
    for shortname,name,ra,dec in data:
      try:
        print db.list("select ra,dec from sources where shortname='{}'".format(shortname)).fetchone(), (ra,dec)
        db.dict("update sources set ra={}, dec={} where shortname='{}'".format(float(ra),float(dec),shortname)) 
      except: print 'No object with shortname '+shortname                       
                                                