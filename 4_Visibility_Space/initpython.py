from IPython.display import Image
from IPython.core.display import HTML
def css_styling():
    styles = open("./styles/custom.css", "r").read()
    return HTML(styles)

print "Config loaded"
#css_styling()

# CSS styling: 
#read http://stackoverflow.com/questions/18024769/adding-custom-styled-paragraphs-in-markdown-cells

