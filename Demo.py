import gridlang

##Create an abstact glyph (A glyph which itself is a circuit of glyphs)
harmonyglyph=abstractglyph(grid({}, ##Has no constants
         {
             (0,0):flowglyph(None,None,1,None), #Output is input, feeds the result to the right with 1:1 weight
             (1,0):amplifierglyph(pi,None,None,1,None), #Receives the value from the flow glyph and amplifies it by pi, feeds the result to the right with 1:1 weight
             (2,0):amplifierglyph("N",None,None,1,None), #Recieves the input from the previous amplifier an multiplies it by the variable N, feeds the result to the right with 1:1 weight
             (3,0):circleglyph(0,None,None,y,None), #A circle glyph has its azimuth incremented by the input from the amplifier glyph, feeds the sine wave of the azimuth to the right
             (4,0):amplifierglyph("V",None,None,None,1), #Amplifies the Y value of the circle glyph by the variable V (for volume or velocity) feeds it down with 1:1 correspondance
             (4,1):traceglyph("wave"), Output the value to a varible named "wave"
               }),
                (0,0), #any values inputted to the glyph go to node (0,0) the initial flow glyph
                ["N","V"],#there are two variables, N and V (these are defined on initialising the glyph)
                down="wave") ##The value of traceglyph("wave") will be fed to the grid space below any instance of this glyph
"""This custom glyph takes the form
F>A>A>C>A
        ↓
        T
"""

#Program Definition
myprogram=grid({"F":110},
     {
         (0,0):amplifierglyph("F",None,None,None,1),
         (1,0):amplifierglyph(1/44100,1,None,None,None),
         (2,0):logglyph(2,1,None,None,None),
         (0,1):flowglyph(None,None,1,1),
         (1,1):flowglyph(None,None,1,1),
         (2,1):flowglyph(None,None,1,1),
         (3,1):flowglyph(None,None,1,1),
         (4,1):flowglyph(None,None,None,1),
         (0,2):harmonyglyph.new(1,1),
         (1,2):harmonyglyph.new(2,1/2),
         (2,2):harmonyglyph.new(3,1/3),
         (3,2):harmonyglyph.new(4,1/4),
         (4,2):harmonyglyph.new(5,1/5),
         (0,3):flowglyph(None,None,1,None),
         (1,3):flowglyph(None,None,1,None),
         (2,3):flowglyph(None,None,1,None),
         (3,3):flowglyph(None,None,1,None),
         (4,3):flowglyph(None,None,1,None),
         (5,3):traceglyph("wave")      
})

#Import matplotlib plotting
import matplotlib.pyplot as plt
o=[]
for i in range(4410):
    myprogram.calculatepaths((1,0))
    myprogram.pipein((1,0),1)
    o.append(myprogram.glyphs[(5,3)].value)
    #myprogram.traces()
    #[myprogram.glyphs[x].value for x in myprogram.glyphs]
    myprogram.next()
#Run the program 4410 frames (a tenth of a second at 44100HZ) and add the result of traceglyph("wave") to the list `o`

#plot and show the list `o` upon completion
plt.plot(o)
plt.show()
