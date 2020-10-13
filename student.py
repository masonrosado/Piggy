#!/usr/bin python3
from collections import OrderedDict
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 83.5
        self.SAFE_DISTANCE = 250
        self.CLOSE_DISTANCE = 125
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        """A higher-ordered algorithm to make your robot dance"""
        if not self.safe_to_dance():
            return False #shutdown
        for x in range(4):  
            self.shuffle()
            self.skipp()
            self.spin_dizzy()
            self.for_back()
            self.break_neck()
            self.swiggly()
            self.break_neck()
            self.backward_shimmey()
        
        
        
        
    def spin_dizzy(self):
        """"spin both ways"""
        self.right(primary=90, counter=-90)
        time.sleep(4)
        self.stop()
        self.left(primary=90, counter=-90)
        time.sleep(4)
        self.stop()
    
    
    def for_back(self):
        """forward/back"""
        self.fwd()
        time.sleep(2)
        self.stop()
        self.back()
        time.sleep(2)
        self.stop()

    
    def break_neck(self):
        """look left/right"""
        self.servo(1000) 
        time.sleep(1) 
        self.servo(2000)
        time.sleep(1) 
        self.servo(1500)
        self.stop()

    
    def swiggly(self):
        """S-shape"""
        self.fwd(left=90, right=45)
        time.sleep(1)
        self.fwd(left=45, right=90)
        time.sleep(1)
        self.fwd(left=90, right=45)
        time.sleep(1)
        self.fwd(left=45, right=90)
        time.sleep(1)
        self.fwd(left=45, right=0)
        time.sleep(.25)
        self.stop()
        
    
    def shuffle(self): 
        """Quinn Shuffle from discord"""   
        for x in range(12):
            self.right(primary=-60, counter=0)
            time.sleep(.1)
            self.left(primary=-60, counter=0)
            time.sleep(.1)
        self.stop()

    
    def skipp(self):
        """Brennan's skipp move from discord"""
        for x in range(4):
            self.fwd(right=100, left=100)
            time.sleep(.5)
            self.servo(1000)
            time.sleep(.1)
            self.servo(2000)
            time.sleep(.1)
            self.fwd(right=-100, left=-100)
            time.sleep(.1)
            self.servo(-1000)
            self.stop()

   
    def backward_shimmey(self):
        """Haydn's backward shimmey from discord"""
        for x in range(6):
            self.right(primary=-70, counter=-30)
            time.sleep(.5)
            self.left(primary=-70, counter=-30)
            time.sleep(.5)
        self.stop()

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        #check for all fil/early-termination conditions
        for _ in range(4):
            if self.read_distance() < 300:
                print("not safe to dance!")
                return False
            else:
                self.turn_by_deg(90)
        #after all checks have been done, we deduce its safe to dance
        print("Dance on!")
        return True


    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 12):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()
        #sort the scan data for easier analysis
        self.scan_data = OrderedDict(sorted(self.scan_data.items()))
    
    def right_or_left(self):
        """Should I turn left or right?
            Returns a 'r' or 'l' based on scan data"""
        self.scan()

        right_sum = 0
        right_avg = 0
        left_sum = 0
        left_avg = 0

        #analyze scan results
        for angle in self.scan_data:
        #average up the distances on the right side
            if angle < self.MIDPOINT:
                right_sum+= self.scan_data[angle]
                right_avg += 1
            else:
                left_sum +=self.scan_data[angle]
                left_avg += 1

        #calculate averages
        left_avg = left_sum / left_avg
        right_avg = right_sum / right_avg

        if left_avg > right_avg:
            return 'l'
        else:
            return 'r'
        
            
    
    
    
    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        #scan area in front of robot
        self.scan()
        
        
        #Figure ot how many obstacles there were
        see_an_object = False
        count = 0
    def quick_check(self):

        #print results
        for angle in self.scan_data:
            dist = self.scan_data[angle]
            if dist < self.SAFE_DISTANCE and not see_an_object:
                see_an_object = True
                count += 1
                print(" There's a body in the road")
            elif dist > self.SAFE_DISTANCE and see_an_object:
                    see_an_object = False
                    print("All clear")
            print("ANGLE: %d | DIST: %d" % (angle, dist))
        print("\nI saw %d objects" % count)

        """Moves the servo to three angles and performs a distance check"""
        #loop three times and moce the servo 
        for ang in range(self.MIDPOINT - 100, self.MIDPOINT+101, 100):
            self.servo(ang)
            time.sleep(.05)
            if self.read_distance() < self.SAFE_DISTANCE:
                return False
        #if the three-part check didn't freak out
        return True

    def turn_until_clear(self):
        """ Rotate left until no obstacle is seen"""
        print("Rotating until lane is clear")
        #make sure robot is looking straigh
        self.servo(self.MIDPOINT)
        while self.read_distance() < self.SAFE_DISTANCE:
            self.left(primary=40,counter=-40)
            time.sleep(.05)
        #stop motion before ending method
        self.stop()

    def nav(self):
        """ Top Gun Initiative """
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        

        while True:
            if not self.quick_check():
                self.stop()
                #self.turn_until_clear()
                if 'l' in self.right_or_left():
                    self.turn_by_deg(-45)
                else: 
                    self.turn_by_deg(45)
            else:
                self.fwd()

        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
