from IPython.core.display import HTML
def css_styling():
    styles = open("../style/course.css", "r").read()
    print "CSS Config loaded"
    return HTML(styles)

#css_styling()

# CSS styling: 
#read http://stackoverflow.com/questions/18024769/adding-custom-styled-paragraphs-in-markdown-cells

