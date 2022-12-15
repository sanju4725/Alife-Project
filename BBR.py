
import robot, time, random 
from controller import Camera


# Initilise the robot wheel driver
wheels = robot.Wheels(4, 16)

# Initialise the Ground sensor
gnd1 = robot.IR(34)

# Initialise the range sensor. Connect Echo pins to IO12 and IO18,
# Trig pins to IO13 and IO19
range1 = robot.HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=30000)
range2 = robot.HCSR04(trigger_pin=18, echo_pin=19, echo_timeout_us=10000)
# To reduce the range, reduce the echo_timeout value, 


# Parameters
BLACK_THRESHOLD = 600
HIGH_SP = 20
LOW_SP = 0
MED_SP = -10
TURN_AMOUNT = 6 # Update cycle intervals (0.1secs)
UPDATE_PERIOD = 100 # msec, Update cycle time
AVOID_DISTANCE = 150 # In mm
HUNGER =1000
THIRST= 1000
SLEEP = 1000
onLine=0  
### Variables
 # Start with robot in FORWARD state




camera = Camera("camera")
camera.enable(UPDATE_PERIOD)

def eating():
 global HUNGER
 if HUNGER < 1000:
      HUNGER +=30
     
     
def sleeping():
 global SLEEP   
 if SLEEP < 1000:
      SLEEP+=10
     
def drinking():
 global THIRST
 if THIRST < 1000:
      THIRST +=50
     
     
def alive():
    if SLEEP <=0:
        return False
    elif HUNGER <=0:
        return False
    elif THIRST <=0:
        return False
    else:
        return True
        
def meta():
    global SLEEP,HUNGER,THIRST
    SLEEP -=1
    HUNGER -=0.2
    THIRST -=0.2
    #print(SLEEP, HUNGER, THIRST)
            
def cCamera():
    x=0
    y=0
    red=0
    blue=0
    green=0
    width =camera.getWidth()
    height=camera.getHeight()
    cameraData = camera.getImage()
    while x < width:          
        while y < height:
            x+=1
            y+=1
            red += Camera.imageGetRed(cameraData, camera.getWidth(), x,y)        
            blue += Camera.imageGetBlue(cameraData, camera.getWidth(), x, y)
            green += Camera.imageGetGreen(cameraData, camera.getWidth(), x, y)

def Behaviour0():
        one= random.randint(0,20)
        two= random.randint(0,20)
        move(one,two)
#v.basic random walk        
        
        
def Behaviour1():       
     x=0
     while x<10 and robot.step(UPDATE_PERIOD) !=-1:
         updateSensors()
         LEFT, RIGHT = -20,20
         wheels.wheelspds(LEFT,RIGHT)
         updateSensors() 
         move(LEFT,RIGHT)
         x+=1        
#turn around if solid object in front
def Behaviour2():
     x=0
     while x<10 and robot.step(UPDATE_PERIOD) !=-1:
         updateSensors()
         LEFT, RIGHT = 0,20
         wheels.wheelspds(LEFT,RIGHT)
         updateSensors() 
         move(LEFT,RIGHT)
         if r2 < 100 and r1 < 100:
            Behaviour1()
         x+=1  
         
def Behaviour3():
     x=0
     while x<10 and robot.step(UPDATE_PERIOD) !=-1:
         updateSensors()
         LEFT, RIGHT = 20,0
         wheels.wheelspds(LEFT,RIGHT)
         updateSensors() 
         move(LEFT,RIGHT)
         if r2 < 100 and r1 < 100:
            Behaviour1()
         x+=1         
         
def Behaviour4():
      global onLine 
      onLine =1
      wheels.wheelspds(10,10)       
      if r1 < 100 and r2 > 100:
           Behaviour3()         
      elif r1 > 100 and r2 < 100:
            Behaviour2()           
      elif r1 < 100 and r2 < 100:
            Behaviour1()   
            
def Behaviour5(): 
    global onLine
    onLine=0
    y = random.randint(10,20)
    x=0
    while x<y and g1>=800 and robot.step(UPDATE_PERIOD) !=-1:  
      wheels.wheelspds(-10,10) 
      updateSensors() 
      x+=1
      if r1 < 100 and r2 > 100:
           Behaviour3()         
      elif r1 > 100 and r2 < 100:
            Behaviour2()           
      elif r1 < 100 and r2 < 100:
            Behaviour1()        
             
                 
        
def updateSensors():         
     global r1 
     global g1 
     global r2 
     r1 = range1.distance_mm()#mm()
     g1 = gnd1.getIR()
     r2 = range2.distance_mm()#mm()
     meta()
def move(L,R): 
  LW = L
  RW = R       
  if LW > HIGH_SP:
      LW = HIGH_SP
  if RW > HIGH_SP:
      RW = HIGH_SP  
  wheels.wheelspds(LW, RW)





while robot.step(UPDATE_PERIOD) != -1 and alive() != False: # Runs forever. 
    # step() function implenets variable delay fir regular iteration period
    # In Webots simulator, also updates sensors and devices in aimulated world 
    camera = Camera("camera")
    camera.enable(UPDATE_PERIOD)
    try: 
        # Set update cycle period
        #delay =  time.time() + UPDATE_PERIOD #time.ticks_ms() + UPDATE_PERIOD # Delay in ms
        
                ## States and transition trigger rules
        cCamera()
             
        updateSensors()
        if g1>=800 and onLine ==1:
            Behaviour5()
        elif g1<800:
            Behaviour4()
        elif r1 < 100 and r2 > 100:
           Behaviour3()         
        elif r1 > 100 and r2 < 100:
            Behaviour2()           
        elif r1 < 100 and r2 < 100:
            Behaviour1()       
        else:
            Behaviour0()
            
        meta()
  
    except KeyboardInterrupt: # Will break out of while loop if Ctrl+C pressed.
        break
wheels.wheelspds(0, 0)
