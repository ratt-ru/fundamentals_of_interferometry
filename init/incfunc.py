#!/usr/bin/python

#Created: sirothia@gmail.com 20170207
#for label and ref for use in ipython notebook

from ipywidgets import widgets

##########################
#function for giving the filename
##########################
def init_ipyref_filename( ):
    fname='../data/ipyref.txt'
    return fname 
##########################

##########################
#function for incrementing approrpiate counter, not to be used directly the user
##########################
def increment_ipyrefcnt(sdict, cntname):

    nerr=0
    
    if cntname=='chapter' : use_cnt='chapter_cnt'
    elif cntname=='section' :  use_cnt='section_cnt'
    elif cntname=='subsection' :  use_cnt='sectionl1_cnt'
    elif cntname=='subsubsection' :  use_cnt='sectionl2_cnt'
    elif cntname=='subsubsubsection' : use_cnt='sectionl3_cnt'
    elif cntname=='figure' : use_cnt='figure_cnt'
    elif cntname=='equation' : use_cnt='equation_cnt'
    elif cntname=='table' : use_cnt='table_cnt'
    else : nerr+=1

    if nerr!=0 : 
        print "increment_ipyrefcnt=>  Allowed: chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table"
        print "increment_ipyrefcnt=> Requested:", cntname

    if nerr==0 and sdict.has_key(use_cnt) :
        sdict[use_cnt]+=1
    else :
        print "increment_ipyrefcnt=> No counter by name", use_cnt
        print "increment_ipyrefcnt=> Allowed: chapter_cnt, section_cnt, sectionl1_cnt, sectionl2_cnt, sectionl3_cnt, equation_cnt, figure_cnt, table_cnt"
        nerr+=1
    
    if nerr==0:
        if sdict['chapter_cnt'] != sdict['lastchapter_cnt'] :
            sdict['section_cnt']=sdict['sectionl1_cnt']=sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=0
            sdict['equation_cnt']=sdict['figure_cnt']=sdict['table_cnt']=0
            sdict['lastchapter_cnt']=sdict['chapter_cnt']
        
        if sdict['section_cnt'] != sdict['lastsection_cnt'] :
            sdict['sectionl1_cnt']=sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=0
            sdict['lastsection_cnt']= sdict['section_cnt']
        
        if sdict['sectionl1_cnt'] != sdict['lastsectionl1_cnt'] :
            sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=0
            sdict['lastsectionl1_cnt']= sdict['sectionl1_cnt']

        if sdict['sectionl2_cnt'] != sdict['lastsectionl2_cnt'] :
            sdict['sectionl3_cnt']=0  
            sdict['lastsectionl2_cnt']= sdict['sectionl2_cnt']
        
    return nerr
##########################


##########################
#for creating the label use
#sdict is internal : not to be used
#cntname : chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table
#labelstr : user choice of label, e.g. idstr is used here
#           Advised not use semi-colon in labelstr
#titlestr: can be a title associated with label
##########################
def ipy_label(sdict, cntname, labelstr, titlestr):

    nerr=0      
    
    if sdict['update_ipyref'] and sdict.has_key(labelstr) :
        nerr+=1
        print '[Error] ipy_label =>  The key', labelstr, 'is already present, use unique string in labelstr'
    
    if nerr==0 and sdict['update_ipyref'] : increment_ipyrefcnt( sdict , cntname)

    
    if cntname=='chapter' : tstr='$\mathfrak{C}$ %d' % sdict['chapter_cnt']
    elif cntname=='section' : tstr='$\S$ %d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'])
    elif cntname=='subsection' : tstr='$\S$ %d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'])
    elif cntname=='subsubsection' : tstr='%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'])
    elif cntname=='subsubsubsection' : tstr='%d.%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'], sdict['sectionl3_cnt'])
    elif cntname=='figure' : tstr='Figure %d.%d' % (sdict['chapter_cnt'], sdict['figure_cnt'])
    elif cntname=='equation' : tstr='Equation %d.%d' % (sdict['chapter_cnt'], sdict['equation_cnt'])
    elif cntname=='table' : tstr='Table %d.%d' % (sdict['chapter_cnt'], sdict['table_cnt'])
    else : nerr+=1

        
    if nerr!=0 : print "[Suggestion] ipy_label=> Allowed: chapter, section, sectionl1, sectionl2_cnt, sectionl3_cnt, equation_cnt, figure_cnt, table_cnt"
    
    if nerr==0 and sdict['update_ipyref'] : sdict[labelstr] = '%s %s' % (tstr, titlestr)
    
    if nerr>0 : print "[Error] ipy_label"

    return nerr
##########################


##########################
#A simple function for ipy_ref
#no longer used
##########################
def ipy_sref(sdict, labelstr, stval):
    
    nerr=0
    lstr=labelstr
    lstr=lstr.replace(":", "_")
    if sdict.has_key(labelstr) :
        stval['child'] = widgets.Label(sdict[labelstr])
        stval['class'] = lstr
        if debug_lvl > 10: print 'id', labelstr, 'use class', stval['class']
    else :
        print 'The key', labelstr, 'does not exist'
        nerr+=1

    return nerr
##########################

##########################
#for reference use
#ipy_ref(sdict, labelstr, stval, titlestr='', sdisplay='default', idsub='', debug_lvl=0)
#sdict : is internal not to be used
#stval : is internal not be used
#labelstr : user choice of label, e.g. idstr is used here 
#titlestr : can be a title associated with label
#idsub : use _xxx where xxx is random text that needs to be different every time the reference is used 
#debug_lvl : 0 default, 1 will print the class string to be used for this reference occurance
#            which is combination of idstr and idcntr
#sdisplay: 'default' reference display
#          'intfile' will display reference with internal to file reference symbol
#          'extfile' will display reference with external to file reference symbol
##########################
def ipy_ref(sdict, labelstr, stval, titlestr='', sdisplay='default', idsub='', debug_lvl=0):
    
    nerr=0
    lstr=labelstr+idsub
    lstr=lstr.replace(":", "_")
    if idsub!='' : lstr+idsub
    if sdict.has_key(labelstr) :
        kstrarr=sdict[labelstr].split()
        tstr=kstrarr[0]
        if kstrarr[0]=='Figure' : tstr='Fig.'
        if kstrarr[0]=='Equation' : tstr='Eqn.'
        
        if sdisplay=='extfile' :  ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr + '$\\rightarrow$'
        elif sdisplay=='intfile' :  ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr + '$\\curvearrowright$'
        elif  titlestr!='' : ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr
        else : ustr=sdict[labelstr]
        
        if debug_lvl > 10: print ustr
        stval['child'] = widgets.Label(ustr)
        stval['class'] = lstr
        if debug_lvl > 0: print '[Suggestion] ipy_ref =>  id', labelstr, 'use class', stval['class']
    else :
        print '[Warning] ipy_ref =>  The key', labelstr, 'does not exist'
        nerr+=1
    
    return nerr
##########################

