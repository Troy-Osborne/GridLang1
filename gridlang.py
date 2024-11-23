from __future__ import division
from math import sin,cos,tan,atan2,hypot,pi
from copy import deepcopy
x="x"
y="y"
azimuth="azimuth"
hypot="hypot"
pi=3.141592653

class flowglyph:
    def __init__(self,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.value=0
        self.inpath=0
        
class addglyph:
    def __init__(self,add,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.value=0
        self.add=add
        self.inpath=0

class amplifierglyph:
    def __init__(self,magnitude,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.magnitude=magnitude
        self.value=0
        self.inpath=0
class logglyph:
    def __init__(self,base,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.base=base
        self.value=0
        self.inpath=0
class traceglyph:
    def __init__(self,varname):
        self.varname=varname
        self.value=0
        self.inpath=0
class circleglyph:
    def __init__(self,startangle=0,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.value=startangle
        self.inpath=0
    def setvals(self):
        self.value=self.value%(2*pi)
        self.y=sin(self.value)
        self.x=cos(self.value)
        #self.hypot=hypot(self.x,self.y)
class capacitorglyph:
    def __init__(self,capacity,threshold,dischargepercent=100,left=None,up=None,right=None,down=None):
        self.left=left;self.up=up;self.right=right;self.down=down;
        self.capacity=capacity
        self.threshold=threshold
        self.dischargepercent=dischargepercent
        self.value=0
        self.inpath=0
    

def isnum(obj):
    return isinstance(obj,float) or isinstance(obj,int)
        
        
class grid:
    def __init__(self,constants={},glyphs={}): #glyph {(x,y):glyph..}
        self.constants=constants
        self.glyphs=glyphs
    def pipein(self,pos,value):
        for i in self.glyphs:
            self.glyphs[i].inputs=0
        self.glyphs[pos].value+=value
        self.eminatefrom(pos)
    def makewave(self,inpos,inputwave,tracepoint):
        o=[]
        for i in inputwave:
            self.calculatepaths(inpos)
            self.pipein(inpos,i)
            o.append(self.traces()[tracepoint])
            self.next()
        return o
    def exportsound(self,inpos,inputwave,tracepoint):
        from struct import pack
        import wave
        wav=self.makewave((0,0),[-12 for i in range(44100)],"wave")
        out=wave.open("out.wav","wb")
        out.setparams((1,4,44100,1,"NONE","NONE"))
        for i in wav:
            out.writeframes(pack("l",(2**31-1)*i))

    def drawpath(self):
        s=""
        for j in range(32):
            for i in range(32):
                s+= str(self.glyphs[(i,j)].inpath) if (i,j) in self.glyphs else " "
            s+="\n"
        return s
    def traces(self):
        o={}
        for i in self.glyphs:
            if isinstance(self.glyphs[i],traceglyph):
                o[self.glyphs[i].varname]=deepcopy(self.glyphs[i].value)
        return o
    def next(self):
        for i in self.glyphs:
            g=self.glyphs[i]
            if isinstance(g,flowglyph) or isinstance(g,addglyph) or isinstance(g,amplifierglyph) or isinstance(g,logglyph) or isinstance(g,traceglyph) or isinstance(g,abstractglyph):
                self.glyphs[i].value=0
    def calculatepaths(self,pos,first=True):
        if first:
            for i in self.glyphs:
                self.glyphs[i].inpath=0
        currentglyph=self.glyphs[pos]
        if isinstance(currentglyph,traceglyph):
            currentglyph.inpath+=1
        else:
            if currentglyph.inpath>0:
                currentglyph.inpath+=1
            else:
                currentglyph.inpath+=1
                direction=[i!=None for i in [currentglyph.left,currentglyph.up,currentglyph.right,currentglyph.down]]
                if direction[0]:#left
                    self.calculatepaths((pos[0]-1,pos[1]),False)
                if direction[1]:#up
                    self.calculatepaths((pos[0],pos[1]-1),False)                
                if direction[2]:#right
                    self.calculatepaths((pos[0]+1,pos[1]),False)
                if direction[3]:#down
                    self.calculatepaths((pos[0],pos[1]+1),False)
    def eminatedirection(self,val,dval,np,currentglyph):
        if np in self.glyphs:
                nextglyph=self.glyphs[np]
                if isnum(dval):
                    nextglyph.value+=dval*val
                    nextglyph.inputs+=1
                    if isinstance(nextglyph,circleglyph):
                        nextglyph.setvals()
                    if nextglyph.inputs==nextglyph.inpath:
                        self.eminatefrom(np)
                else:
                    if isinstance(currentglyph,abstractglyph) and dval !=None:
                        nextglyph.value+=currentglyph.traces[dval]
                    if dval==x:
                        nextglyph.value+=currentglyph.x
                    if dval==y:
                        nextglyph.value+=currentglyph.y
                    if dval==azimuth:
                        nextglyph.value+=val
                    if dval!=None:
                        nextglyph.inputs+=1
                        if isinstance(nextglyph,circleglyph):
                            nextglyph.setvals()
                        if nextglyph.inputs==nextglyph.inpath:
                            self.eminatefrom(np)
            
    def eminatefrom(self,pos):
        currentglyph=self.glyphs[pos]
        if isinstance(currentglyph,abstractglyph):
            currentglyph.run()
        if isinstance(currentglyph,traceglyph):
            pass
        else:
            if isinstance(currentglyph,capacitorglyph):                
                if currentglyph.value>currentglyph.capacity:
                    currentglyph.value=currentglyph.capacity
            val=deepcopy(currentglyph.value)
            if isinstance(currentglyph,amplifierglyph):
                mag=currentglyph.magnitude
                if isinstance(mag,str):
                    mag=self.constants[mag]
                val*=mag
            if isinstance(currentglyph,addglyph):
                add=currentglyph.add
                if isinstance(add,str):
                    add=self.constants[add]
                val+=add
            if isinstance(currentglyph,logglyph):
                base=currentglyph.base
                if isinstance(base,str):
                    base=self.constants[base]
                val=base**val
            if isinstance(currentglyph,capacitorglyph):
                threshold=currentglyph.threshold
                dcp=currentglyph.dischargepercent
                if isinstance(threshold,str):
                    threshold=self.constants[threshold]
                if isinstance(dcp,str):
                    dcp=self.constants[dcp]
                dcr=dcp/100
                if val>=threshold:
                    fired=val*dcp/100
                    val*=dcp/100
                else:
                    val=0
                    fired=False
            #left
            leftval=currentglyph.left
            np=(pos[0]-1,pos[1])
            self.eminatedirection(val,leftval,np,currentglyph)
            #up
            upval=currentglyph.up
            np=(pos[0],pos[1]-1)
            self.eminatedirection(val,upval,np,currentglyph)
            #right            
            rightval=currentglyph.right
            np=(pos[0]+1,pos[1])
            self.eminatedirection(val,rightval,np,currentglyph)
            #down                       
            downval=currentglyph.down
            np=(pos[0],pos[1]+1)
            self.eminatedirection(val,downval,np,currentglyph)
            if isinstance(currentglyph,capacitorglyph) and fired!=False:
                currentglyph.value-=fired

class abstractglyph:
    def __init__(self,grid,pipein,variables=["A"],left=None,up=None,right=None,down=None):
        self.grid=grid
        self.pipein=pipein
        self.variables=variables
        self.left=left
        self.up=up
        self.right=right
        self.down=down
        self.value=0
    def new(self,*variables):
        d={}
        for i in range(len(self.variables)):
            d[self.variables[i]]=variables[i]
        self.program=deepcopy(self.grid)
        self.program.constants=d
        return deepcopy(self)
    def run(self):
        self.program.calculatepaths(self.pipein)
        self.program.pipein(self.pipein,self.value)
        self.value=0
        self.traces=self.program.traces()
        self.program.next()        
