#!/usr/bin/python

#20170227: direct display instead of ipywidgets
#20170207: Created sirothia@gmail.com 
#for label and ref for use in ipython notebook

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

    
    if cntname=='chapter' : tstr='\\212D\\0020 %d' % sdict['chapter_cnt']
    elif cntname=='section' : tstr='\\00A7\\0020 %d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'])
    elif cntname=='subsection' : tstr='\\00A7\\0020 %d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'])
    elif cntname=='subsubsection' : tstr='\\00A7\\0020 %d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'])
    elif cntname=='subsubsubsection' : tstr='\\00A7\\0020 %d.%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'], sdict['sectionl3_cnt'])
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
#for reference use
#rstr=ipy_ref(sdict, labelstr, titlestr='', sdisplay='default', idsub='', debug_lvl=0)
#sdict : is internal not to be used
#labelstr : user choice of label, e.g. idstr is used here 
#titlestr : can be a title associated with label
#idsub : use _xxx where xxx is random text that needs to be different every time the reference is used 
#debug_lvl : 0 default, 1 will print the class string to be used for this reference occurance
#            which is combination of idstr and idcntr
#sdisplay: 'default' reference display
#          'intfile' will display reference with internal to file reference symbol
#          'extfile' will display reference with external to file reference symbol
##########################
def ipy_ref(sdict, labelstr, titlestr='', sdisplay='default', idsub='', debug_lvl=0):
    
    rstr='[Error] ipy_ref => HTML string Error check labelstr/idstr or idsub/idcntr'
    nerr=0
    lstr=labelstr
    if idsub!='' : lstr=lstr+idsub
    lstr=lstr.replace(":", "_")
    if sdict.has_key(labelstr) :
        kstrarr=sdict[labelstr].split()
        tstr=kstrarr[0]
        if kstrarr[0]=='Figure' : tstr='Fig.'
        if kstrarr[0]=='Equation' : tstr='Eqn.'
        
        if sdisplay=='extfile' :  ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr + ' \\2192'
        elif sdisplay=='intfile' :  ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr + ' \\21B7'
        elif  titlestr!='' : ustr=tstr + ' ' + kstrarr[1] + ' ' + titlestr
        else : ustr=sdict[labelstr]
        
        if debug_lvl > 10: print ustr
        rstr='<style> .'+lstr+':after {content: "'+ustr+'";} </style>'
        if debug_lvl > 10: print '[Debug] ipy_ref =>  rstr', rstr
        if debug_lvl > 0: print '[Suggestion] ipy_ref =>  id', labelstr, 'use class', lstr
    else :
        print '[Warning] ipy_ref =>  The key', labelstr, 'does not exist'
        nerr+=1
    
    return rstr
##########################

