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
def ipy_glossary_filename( ):
    fname='../0_Introduction/glossary.ipynb'
    return fname 
##########################
def ipy_abbr_filename( ):
    fname='../0_Introduction/abbr.ipynb'
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
    elif cntname=='cite': use_cnt='cite_cnt'
    elif cntname=='glossary' : use_cnt='glossary_cnt'
    elif cntname=='abbr' : use_cnt='abbr_cnt'
    elif cntname=='eref' : use_cnt='eref_cnt'
    elif cntname=='eread' : use_cnt='eread_cnt'
    else : nerr+=1

    if nerr!=0 : 
        print "increment_ipyrefcnt=>  Allowed: chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table, cite, glossary, abbr, eref, eread"
        print "increment_ipyrefcnt=> Requested:", cntname

    if nerr==0 and sdict.has_key(use_cnt) :
        sdict[use_cnt]+=1
    else :
        print "increment_ipyrefcnt=> No counter by name", use_cnt
        print "increment_ipyrefcnt=> Allowed: chapter_cnt, section_cnt, sectionl1_cnt, sectionl2_cnt, sectionl3_cnt, equation_cnt, figure_cnt, table_cnt, cite_cnt, glossary_cnt, abbr_cnt, eref_cnt, eread_cnt"
        nerr+=1
    
    if nerr==0:
        if sdict['chapter_cnt'] != sdict['lastchapter_cnt'] :
            sdict['section_cnt']=sdict['sectionl1_cnt']=sdict['sectionl2_cnt']=sdict['sectionl3_cnt']=0
            sdict['equation_cnt']=sdict['figure_cnt']=sdict['table_cnt']=0
            sdict['cite']=sdict['glossary']=sdict['abbr']=sdict['eref']=sdict['eread']=0
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
#for the script
##########################
def ipy_prjs(prjs_lstr, prjs_tstr='', prjs_ctstr='', prjs_hstr='', prjs_pstr='', prjs_clestr='', mode='ref'):
    
    mlabelstr='var aval=document.getElementById("'+prjs_lstr+'");\
    if(aval!==null){\
    aval.href="'+prjs_hstr+'";\
    aval.title="'+prjs_pstr+'";\
    aval.innerHTML = "'+prjs_tstr+'";\
    }'

    mrefstr='var cval=document.getElementsByClassName("'+prjs_lstr+'");\
    var i;\
    for (i = 0; i < cval.length; i++) {\
    cval[i].href="'+prjs_hstr+'";\
    cval[i].title="'+prjs_pstr+'";\
    cval[i].innerHTML = "'+prjs_ctstr+prjs_clestr+'";\
    }'

    if mode == 'label' : rstr='<script>'+mlabelstr+mrefstr+'</script>'
    else : rstr='<script>'+mrefstr+'</script>'
    
    return rstr
    
    

##########################
#for creating the label use
#sdict is internal : not to be used
#cntname : chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table,
#          cite, glossary, abbr, eref, eread
#labelstr : user choice of label, e.g. idstr is used here
#           Do not use semi-colon in labelstr
#titlestr: can be a title associated with label
#popupstr : the string to display as popup string
#sfilename : the current file name or the href in case of cite, eref, eread 
##########################
def ipy_label(sdict, cntname, labelstr, titlestr, popupstr='', sfilename=''):

    nerr=0      
    if sfilename=='' : print "[Warning] ipy_label => Empty filename"

    rstr='[Error] ipy_label => HTML string Error check labelstr or titlestr'
    
    if sdict['update_ipyref'] and sdict.has_key(labelstr) :
        nerr+=1
        print '[Error] ipy_label =>  The key', labelstr, 'is already present, use unique string in labelstr'
    
    if nerr==0 and sdict['update_ipyref'] : increment_ipyrefcnt(sdict, cntname)

    if cntname=='chapter' : tstr='&#8493 %d' % sdict['chapter_cnt']
    elif cntname=='section' : tstr='&sect %d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'])
    elif cntname=='subsection' : tstr='&sect %d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'])
    elif cntname=='subsubsection' : tstr='&sect %d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'])
    elif cntname=='subsubsubsection' : tstr='&sect %d.%d.%d.%d.%d' % (sdict['chapter_cnt'], sdict['section_cnt'], sdict['sectionl1_cnt'], sdict['sectionl2_cnt'], sdict['sectionl3_cnt'])
    elif cntname=='figure' : tstr='Figure %d.%d' % (sdict['chapter_cnt'], sdict['figure_cnt'])
    elif cntname=='equation' : tstr='Equation %d.%d' % (sdict['chapter_cnt'], sdict['equation_cnt'])
    elif cntname=='table' : tstr='Table %d.%d' % (sdict['chapter_cnt'], sdict['table_cnt'])
    elif cntname=='cite' : tstr='Cite %d.%d' % (sdict['chapter_cnt'], sdict['cite_cnt'])
    elif cntname=='glossary' : tstr='Glossary %d.%d' % (sdict['chapter_cnt'], sdict['glossary_cnt'])
    elif cntname=='abbr' : tstr='Abbr %d.%d' % (sdict['chapter_cnt'], sdict['abbr_cnt'])
    elif cntname=='eref' : tstr='Eref %d.%d' % (sdict['chapter_cnt'], sdict['eref_cnt'])
    elif cntname=='eread' : tstr='Eread %d.%d' % (sdict['chapter_cnt'], sdict['eread_cnt'])
    else : nerr+=1
        
    if nerr!=0 : print "[Suggestion] ipy_label=>  Allowed: chapter, section, subsection, subsubsection, subsubsubsection, equation, figure, table, cite, glossary, abbr, eref, eread"
        
    hstr=labelstr+"href"
    pstr=labelstr+"pstr"
    if nerr==0 and sdict['update_ipyref'] :
        sdict[labelstr] = '%s %s' % (tstr, titlestr)
        sdict[hstr]= sfilename+'#'+labelstr
        sdict[pstr]= popupstr
        if cntname=='cite' or cntname=='eref' or cntname=='eread' : sdict[hstr]= sfilename
        if cntname=='glossary' : sdict[hstr]= ipy_glossary_filename()
        if cntname=='abbr' : sdict[hstr]= ipy_abbr_filename()

    if nerr==0 : rstr=ipy_ref(sdict=sdict, labelstr=labelstr,  idsub='', mode='label', titlestr='', popupstr=popupstr, sfilename=sfilename)

    if nerr>0 : print "[Error] ipy_label"
                
    return rstr
##########################

##########################
#for reference use
#rstr=ipy_ref(sdict, labelstr, titlestr='', sdisplay='default', idsub='', debug_lvl=0)
#sdict : is internal not to be used
#labelstr : user choice of label, e.g. idstr is used here 
#titlestr : can be a title associated with label
#idsub : use _xxx where xxx is random text that needs to be different every time the reference is used 
#mode : ref, label is used only when the function is called from ipy_label
#titlestr : Use the variable if you need to give a new title for display other then when created
#           do change the idsub whenever a new title is used
#popupstr : the string to display as popup string
#sfilename : the current file name or the href in case of cite, eref, eread 
#debug_lvl : 0 default, 1 will print the class string to be used for this reference occurance
#            which is combination of idstr and idcntr
##########################
def ipy_ref(sdict, labelstr,  idsub='', mode='ref', titlestr='', popupstr='', sfilename='', debug_lvl=0):
    
    scntr=['Cite', 'Glossary', 'Abbr', 'Eref', 'Eread']
    
    rstr='[Error] ipy_ref => HTML string Error check labelstr/idstr or idsub/idcntr'
   
    if sdict.has_key(labelstr) :

        hrefstr=''
        hstr=labelstr+"href"
        pstr=labelstr+"pstr"
        lclestr=''

        if sdict.has_key(hstr) : hrefstr=sdict[hstr]
        else : print '[Warning] ipy_ref =>  Href for', labelstr, 'does not exist'
            
        if sfilename!='' :
            if hrefstr.find('http://')>=0 : lclestr=' &#8620'
            elif hrefstr.find(sfilename)>=0 : lclestr=' &#8631'
            else : lclestr=' &#8594'
        else :
            print '[Warning] ipy_ref =>  Empty file name for', labelstr
    
        cltstr=ltstr=sdict[labelstr]
        kstrarr=ltstr.split(' ', 2)
        tstr=kstrarr[0]
        if kstrarr[0] in scntr : cltstr=ltstr=kstrarr[2]
        if kstrarr[0]=='Figure' : tstr='Fig.'
        if kstrarr[0]=='Equation' : tstr='Eqn.'
        
        if idsub!='' : 
            if kstrarr[0] in scntr : cltstr=titlestr
            else : cltstr=tstr + ' ' + kstrarr[1] + ' ' + titlestr
        else : 
            if kstrarr[0] in scntr : cltstr=kstrarr[2]
            else : cltstr=tstr + ' ' + kstrarr[1] + ' ' + kstrarr[2]
            
        tpopupstr=''
        if sdict.has_key(pstr) : tpopupstr=sdict[pstr]
            
        rstr=ipy_prjs(prjs_lstr=labelstr+idsub, prjs_tstr=ltstr, prjs_ctstr=cltstr,\
                      prjs_hstr=hrefstr, prjs_pstr=tpopupstr, prjs_clestr=lclestr, mode=mode)
    else :
        print '[Warning] ipy_ref =>  The key', labelstr, 'does not exist'
    
    return rstr

#################################