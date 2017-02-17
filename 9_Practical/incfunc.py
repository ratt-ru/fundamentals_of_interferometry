#!/usr/bin/python
from ipywidgets import widgets

def init_ipyref_filename( ):
    fname='../data/ipyref.txt'
    return fname 

def increment_ipyrefcnt(sdict, cntname):

    nerr=0
    
    if cntname=='chapter' :
        use_cnt='chapter_cnt'
    elif cntname=='section' :
        use_cnt='section_cnt'
    elif cntname=='subsection' :
        use_cnt='sectionl1_cnt'
    elif cntname=='subsubsection' :
        use_cnt='sectionl2_cnt'
    elif cntname=='subsubsubsection' :
        use_cnt='sectionl3_cnt'
    elif cntname=='figure' :
        use_cnt='figure_cnt'
    elif cntname=='equation' :
        use_cnt='equation_cnt'
    elif cntname=='table' :
        use_cnt='table_cnt'
    else :
        print "increment_ipyrefcnt=>  Allowed: chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table"
        print "increment_ipyrefcnt=> Requested:", cntname
        nerr+=1

    if nerr==0 and sdict.has_key(use_cnt) :
        sdict[use_cnt]+=1
    else :
        print "increment_ipyrefcnt=> No counter by name", use_cnt
        print "increment_ipyrefcnt=> Allowed: chapter_cnt, section_cnt, sectionl1_cnt, sectionl2_cnt, sectionl3_cnt, equation_cnt, figure_cnt, table_cnt"
        nerr+=1
    
    if nerr==0:
        if sdict['chapter_cnt'] != sdict['lastchapter_cnt'] :
            sdict['section_cnt']=sdict['sectionl1_cnt']=sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=1
            sdict['equation_cnt']=sdict['figure_cnt']=sdict['table_cnt']=1
            sdict['lastchapter_cnt']=sdict['chapter_cnt']
        
        if sdict['section_cnt'] != sdict['lastsection_cnt'] :
            sdict['sectionl1_cnt']=sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=1
            sdict['lastsection_cnt']= sdict['section_cnt']
        
        if sdict['sectionl1_cnt'] != sdict['lastsectionl1_cnt'] :
            sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=1
            sdict['lastsectionl1_cnt']= sdict['sectionl1_cnt']

        if sdict['sectionl2_cnt'] != sdict['lastsectionl2_cnt'] :
            sdict['sectionl3_cnt']=1  
            sdict['lastsectionl2_cnt']= sdict['sectionl2_cnt']
        
    return

def ipy_label(sdict, cntname, labelstr, titlestr):

    #if sdict.has_key(labelstr) :
    nerr=0  
    
    if cntname=='chapter' :
        use_cnt='chapter_cnt'
        tstr='%d' % sdict['chapter_cnt']
    elif cntname=='section' :
        use_cnt='section_cnt'
        tstr='%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'])
    elif cntname=='subsection' :
        use_cnt='sectionl1_cnt'
        tstr='%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['subsection_cnt'])
    elif cntname=='subsubsection' :
        use_cnt='sectionl2_cnt'
        tstr='%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['subsection_cnt'], sdict['subsubsection_cnt'])
    elif cntname=='subsubsubsection' :
        use_cnt='sectionl3_cnt'
        tstr='%d.%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['subsection_cnt'], sdict['subsubsection_cnt'], sdict['subsubsubsection_cnt'])
    elif cntname=='figure' :
        use_cnt='figure_cnt'
        tstr='Figure %d.%d' % (sdict['chapter_cnt'], sdict['figure_cnt'])
    elif cntname=='equation' :
        use_cnt='equation_cnt'
        tstr='Equation %d.%d' % (sdict['chapter_cnt'], sdict['equation_cnt'])
    elif cntname=='table' :
        use_cnt='table_cnt'
        tstr='Table %d.%d' % (sdict['chapter_cnt'], sdict['table_cnt'])
    else :
        print "ipy_label=> Allowed: chapter, section, sectionl1, sectionl2_cnt, sectionl3_cnt, equation_cnt, figure_cnt, table_cnt"
        nerr+=1
    
    if nerr==0 and sdict['update_ipyref'] :
        sdict[labelstr] = '%s %s' % (tstr, titlestr)
        increment_ipyrefcnt( sdict , cntname)
    
    if nerr>0 :
        print "ipy_label=> Error"

    return nerr

def ipy_ref(sdict, labelstr, stval):
    
    nerr=0
    lstr=labelstr
    lstr=lstr.replace(":", "_")
    if sdict.has_key(labelstr) :
        stval['child'] = widgets.Label(sdict[labelstr])
        stval['class'] = lstr
        print 'id', labelstr, 'use class', stval['class']
    else :
        print 'The key', labelstr, 'does not exist'
        nerr+=1

    return nerr
