import numpy as np
import pylab as plt
plt.rcParams['figure.figsize'] = (5, 7) #(width, height)

def draw_orion():
    names = ["Center","Betelgeuse","Rigel","Bellatrix","Mintaka","Alnilam","Alnitak","Saiph"]
    RA = [5+30.0/60,5+55.0/60+10.3053/3600,5+14.0/60+32.272/3600,5+25.0/60+7.9/3600,5+32.0/60+0.4/3600,5+36.0/60+12.8/3600,5+40.0/60+45.5/3600,5+47.0/60+45.4/3600]
    DEC = [0,7+24.0/60+25.426/3600,-8-12.0/60-5.91/3600,6+20.0/60+59.0/3600,-17.0/60-57.0/3600,-1-12.0/60-6.9/3600,-1-56.0/60-34.0/3600,-9-40.0/60-11.0/3600]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(RA[0],DEC[0],"bx")
    plt.hold("on")
    plt.plot(RA[1],DEC[1],"ro")
    plt.plot(RA[2],DEC[2],"co")
    plt.plot(RA[3:],DEC[3:],"go")   
    counter = 1
    for xy in zip(RA[1:], DEC[1:]):                                              
        ax.annotate(names[counter], xy=xy, textcoords='offset points',horizontalalignment='left',
            verticalalignment='top')  
        counter = counter + 1
    plt.xlim([5,6])
    plt.xlabel("Right Ascension [h]")
    plt.ylim([-11,11])
    plt.ylabel("Declination [degrees]")
    plt.gca().invert_xaxis()
    plt.grid()
    plt.savefig('orion_fig.png')
    plt.show()  

    C_RA = RA[0]*(np.pi/12)
    print "C_RA = ",C_RA
    B_RA = RA[1]*(np.pi/12)
    print "B_RA = ",B_RA
    R_RA = RA[2]*(np.pi/12)
    print "R_RA = ",R_RA

    delta_B_RA = B_RA - C_RA 
    print "delta_B_RA = ",delta_B_RA
    delta_R_RA = R_RA - C_RA
    print "delta_R_RA = ",delta_R_RA

    C_DEC = DEC[0]*(np.pi/180)
    print "C_DEC = ",C_DEC
    B_DEC = DEC[1]*(np.pi/180)
    print "B_DEC = ",B_DEC
    R_DEC = DEC[2]*(np.pi/180)
    print "R_DEC = ",R_DEC

    delta_B_DEC = B_DEC - C_DEC

    l_B = np.cos(B_DEC)*np.sin(delta_B_RA)
    print "l_B = ",l_B*(180/np.pi)
    m_B = np.sin(B_DEC)*np.cos(C_DEC)-np.cos(B_DEC)*np.sin(C_DEC)*np.cos(delta_B_RA)
    print "m_B = ",m_B*(180/np.pi)    

    l_R = np.cos(R_DEC)*np.sin(delta_R_RA)
    print "l_R = ",l_R*(180/np.pi)
    m_R = np.sin(R_DEC)*np.cos(R_DEC)-np.cos(R_DEC)*np.sin(C_DEC)*np.cos(delta_R_RA)
    print "m_R = ",m_R*(180/np.pi)
    
    theta_1 = np.sqrt(l_B**2+m_B**2)*(180/np.pi)
    theta_2 = np.arcsin(np.sqrt(l_B**2+m_B**2))*(180/np.pi)
    theta_3 = np.arccos(np.cos(delta_B_RA)*np.cos(delta_B_DEC))*(180/np.pi)
    theta_4 = np.sqrt(delta_B_RA**2 + delta_B_DEC)*(180/np.pi) 

    print "theta_1 = ", theta_1 
    print "theta_2 = ", theta_2 
    print "theta_3 = ", theta_3
    print "theta_4 = ", theta_4    


    RA_rad = np.array(RA)*(np.pi/12)
    DEC_rad = np.array(DEC)*(np.pi/180)
    RA_delta_rad = RA_rad-RA_rad[0]

    l = np.cos(DEC_rad)*np.sin(RA_delta_rad)*(180/np.pi)
    m = (np.sin(DEC_rad)*np.cos(DEC_rad[0])-np.cos(DEC_rad)*np.sin(DEC_rad[0])*np.cos(RA_delta_rad))*(180/np.pi)
    print "l = ",l
    print "m = ",m
    plt.hold("off")
    plt.xlim([-8,8])
    plt.ylim([-10,10])
    plt.xlabel("$l$ [degrees]")
    plt.ylabel("$m$ [degrees]")
    plt.plot(l[0],m[0],"bx")
    plt.hold("on")
    plt.plot(l[1],m[1],"ro")
    plt.plot(l[2],m[2],"co")
    plt.plot(l[3:],m[3:],"go") 
    
    counter = 1
    for xy in zip(l[1:], m[1:]):                                              
        ax.annotate(names[counter], xy=xy, textcoords='offset points',horizontalalignment='left',
            verticalalignment='top')  
        counter = counter + 1
    plt.gca().invert_xaxis()
    plt.grid()
    plt.show()

if  __name__=="__main__":
    draw_orion()
    
