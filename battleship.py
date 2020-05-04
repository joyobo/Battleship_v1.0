from kivy.app import App
from kivy.uix.label import Label
# uix is a folder in kivy. label is a class 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.utils import *
import random
import copy

Builder.load_string("""
<Setup>
    FloatLayout:
        id: overall
        Label:
            text: "Battle Ship"
            font_size: ((root.width**2 + root.height**2) / 23**4)+60
            pos_hint: {"x":0.325, "y":0.83}
            size_hint: 0.35, 0.15
        
        Label:
            text: "(4px) Battleship\\n(3px) Cruiser\\n(2px) Destroyer\\n(1px) Submarine"
            font_size: ((root.width**2 + root.height**2) / 23**4)+20
            pos_hint: {"x":-0.02, "y":0.82}
            size_hint: 0.35, 0.15
            
        Label:
            id: labelupdate
            text: "{}\\n{}\\n{}\\n{}".format(1, 2, 3, 4)
            font_size: ((root.width**2 + root.height**2) / 23**4)+20
            pos_hint: {"x":0.11, "y":0.82}
            size_hint: 0.35, 0.15
            
        Button:
            text: "Place"
            font_size: ((root.width**2 + root.height**2) / 23**4)+20
            pos_hint: {"x":0.87, "y":0.1}
            size_hint: 0.1, 0.15
            on_press: root.checkship(root.shipchoose)
            
        GridLayout:
            id: grid
            size: min(root.height * 0.7, root.width), min(root.height * 0.7, root.width)
            size_hint: None, None
            pos_hint: {'x': (0.5-((min(root.height * 0.7, root.width)/root.width)/2)),'y': 0.05}
            cols: 10
            rows: 10
            
<Gamescreen> 
    FloatLayout:
        id: overallscreen
        Label:
            text: "Battle Ship"
            font_size: ((root.width**2 + root.height**2) / 23**4)+60
            pos_hint: {"x":0.325, "y":0.83}
            size_hint: 0.35, 0.15

        Label:
            text: "Your Border"
            font_size: ((root.width**2 + root.height**2) / 23**4)+30
            pos_hint: {"x":0.125, "y":0.72}
            size_hint: 0.35, 0.15
            
        GridLayout:
            id: yourborder
            size: min(root.height * 0.7, root.width), min(root.height * 0.7, root.width)
            size_hint: None, None
            pos_hint: {'x': (0.3-((min(root.height * 0.7, root.width)/root.width)/2)),'y': 0.05}
            cols: 10
            rows: 10
            
        Label:
            text: "(4px) Battleship\\n(3px) Cruiser\\n(2px) Destroyer\\n(1px) Submarine"
            font_size: ((root.width**2 + root.height**2) / 23**4)+10
            pos_hint: {"x":-0.01, "y":0.82}
            size_hint: 0.35, 0.15
            
        Label:
            id: myshipupdate
            text: "{}\\n{}\\n{}\\n{}".format(1, 2, 3, 4)
            font_size: ((root.width**2 + root.height**2) / 23**4)+10
            pos_hint: {"x":0.08, "y":0.82}
            size_hint: 0.35, 0.15
       
        Label:
            text: "Enemy's Border"
            font_size: ((root.width**2 + root.height**2) / 23**4)+30
            pos_hint: {"x":0.531, "y":0.72}
            size_hint: 0.35, 0.15
            
        GridLayout:
            id: enemyborder
            size: min(root.height * 0.7, root.width), min(root.height * 0.7, root.width)
            size_hint: None, None
            pos_hint: {'x': (0.7-((min(root.height * 0.7, root.width)/root.width)/2)),'y': 0.05}
            cols: 10
            rows: 10
            
        Label:
            text: "(4px) Battleship\\n(3px) Cruiser\\n(2px) Destroyer\\n(1px) Submarine"
            font_size: ((root.width**2 + root.height**2) / 23**4)+10
            pos_hint: {"x":0.6, "y":0.82}
            size_hint: 0.35, 0.15
            
        Label:
            id: eneshipupdate
            text: "{}\\n{}\\n{}\\n{}".format(1, 2, 3, 4)
            font_size: ((root.width**2 + root.height**2) / 23**4)+10
            pos_hint: {"x":0.7, "y":0.82}
            size_hint: 0.35, 0.15

<Levelscreen>       
    GridLayout:
        id: levelgrid
        size: min(root.height * 0.7, root.width*0.7), min(root.height * 0.7, root.width*0.7)
        size_hint: None, None
        pos_hint: {'x': (0.3-((min(root.height * 0.7, root.width)/root.width)/2)),'y': 0.05}
        cols: 1
        rows: 3         
""")
# default items    
numid = ["{}".format([i,j]) for i in range(1,11) for j in range(1,11)]
nameship = {4:'Battleship(4)', 3: 'Cruiser(3)', 2: 'Destroyer(2)', 1:'Submarine(1)'}

#Boolean and surrlist
#creates a list of surr and checks ship surrounding
def checksurr(shipchooseid, checking=False, shipplaced=[]):
    #reset the surrlist everytime this function is called
    surrlist = []
    length = len(shipchooseid)
    #for each button chosen
    for i in range(length):
        row, col = shipchooseid[i]
        #append all 8 surr button id/num
        surr1 =  [[row-1,col],[row-1,col+1],[row,col+1],[row+1,col+1],[row+1, col],[row+1,col-1],[row,col-1],[row-1,col-1]]
        surr1 = [surr1[j] for j in range(len(surr1)) if surr1[j][0] >= 1 and surr1[j][0] <= 10 and surr1[j][1] >= 1 and surr1[j][1] <= 10]
        print("{}, surr1:{}".format(i,surr1))
        surr1 = [surr1[k] for k in range(len(surr1)) if surr1[k] not in shipchooseid and surr1[k] not in surrlist]

        #finally add this list to your surrlist
        surrlist = surrlist + surr1
        surrlist.sort()
        print("{}, surrlist:{}".format(i,surrlist))
        
    print(surrlist)
    
    if checking == True:
        for every in surrlist:
            for key, val in shipplaced.items():
                if val:
                    for num in val:
                        if every in num[0]:
                            return False, []
            
        return True,surrlist
    else:
        return surrlist
    
class Setup(Screen):
    #keep track of avaiability of ships
    shipavb = {'Battleship(4)': 1, 'Cruiser(3)': 2, 'Destroyer(2)': 3, 'Submarine(1)': 4}
    #to get ship name from length
    #temporary dictionary that appends the button (id/num as keys and instance as values) that are chosen (will be reset when ship is placed)
    shipchoose = {}
    #ships that are CONFIRMED and placed down
    finalship = {'Battleship(4)': [], 'Cruiser(3)': [], 'Destroyer(2)': [], 'Submarine(1)': []}    
    
    #for enemy ships
    availid = [[i,j] for i in range(1,11) for j in range(1,11)]
    finalenship = {'Battleship(4)': [], 'Cruiser(3)': [], 'Destroyer(2)': [], 'Submarine(1)': []}

    def on_pre_enter(self):
        #create a dictionary of buttons with their id num and id
        for i in range(100):
            self.btn = ToggleButton(id=numid[i], height = 0.001, width = 0.001)
            self.btn.bind(on_press=self.update)
            self.ids.grid.add_widget(self.btn)
     
    #invoked when toggle button is clicked - checks the state of the togglebutton
    def update(self, instance):
        #on_press meaning that the togglebutton is clicked already and state changes from 'normal' to 'down'
        #button is SELECTED
        if instance.state == 'down':
            print("clicked toggle button: ",self.shipchoose)
            self.shipchoose[instance.id] = instance
            instance.background_color = [0,0,0,0]
            instance.text = ''
            
        #toggle button changes from 'down' to 'normal'
        #button is DESELECTED
        if instance.state == 'normal':
            instance.background_color = [1,1,1,1]
            del self.shipchoose[instance.id]

    #when the 'Place' button is clicked
    #input is self.shipchoose dictionary
    def checkship(self,shipchoose):
        #Boolean value (True-ship is qualified to be placed ; False-ship did not meet requirements - error popups needed)
        need_reset = True
        length = len(shipchoose)
        shipchooseid =[]
        # get the indexes in int (instead of string)
        for a in shipchoose.keys():
            r,c = a.strip("[]'").split(",") 
            r,c = int(r),int(c)
            shipchooseid.append([r,c])
        shipchooseid.sort()
        
        #checks that the ship length is right
        if length >= 1 and length <=4:
            #checks that the ship is horizontal or vertical (and not in other arrangements)
            if self.checkori(shipchooseid):
                bool_checksurr, surrlist = checksurr(shipchooseid, True, self.finalship)
                if bool_checksurr:
                    #checks that ship of this certain length i still available
                    if self.checkavail(length):
                        #only if all this requirements are passed then there isnt a need to restart
                        need_reset = False
                else:
                    pop = Popup(title='Invalid Placement', content=Label(text='Ships cannot be placed right beside other ships.\nShips require at least a space between them.'), size_hint=(None,None),size=(400,400))
                    pop.open()
        else:
            pop = Popup(title='No ship of size {}'.format(length), content=Label(text='Ships are only of sizes 1, 2, 3 or 4.'), size_hint=(None,None),size=(400,400))
            pop.open()
            
        #Requirements not reached - put back the buttons
        if need_reset:
            for key,val in shipchoose.items():
                val.state = 'normal'
                val.background_color = [1,1,1,1]
        
        #requirements reached - store into self.finalship (its location and surr) and add a ship image        
        if not need_reset:
            ship_name = nameship[length]
            newval = self.finalship[ship_name]
            shipnsurr = [shipchooseid,surrlist]
            newval.append(shipnsurr)
            self.finalship[ship_name] = newval
            print(self.finalship)
            #change image button to ship_unit.png
            for key,val in shipchoose.items():
                val.add_widget(Image(source = 'ship_unit.png', size = (val.width, val.height), pos = val.pos))
                #so that the buttons with ship placed will be disabled
                val.disabled = True
        
        #reset the dictionary back to empty
        self.shipchoose = {}
        
        if self.shipavb["Battleship(4)"] == 0 and self.shipavb['Cruiser(3)'] == 0 and self.shipavb['Destroyer(2)'] == 0 and self.shipavb['Submarine(1)']==0:
            print("nextscreen")
            startbut = Button(text='   Start\nBattling !', font_size=50)
            startbut.bind(on_release = self.nextscreen)
            self.ids.overall.add_widget(startbut)            

# Helper functions for checkship --------------------------------------------------------------------------------------------------    
    
    #Boolean function
    #checks if ships are in horizontal or vertical placement (no diagonals/separated)
    def checkori(self, shipchooseid):        
        #Boolean value
        ori = True
        
        #1 button chose
        if len(shipchooseid) == 1:
            return ori
        
        #more than 1 buttons chose
        else:
            #horizontal
            #checks that ships num/id are consecutive
            for j in range(len(shipchooseid)-1):
                if int(shipchooseid[j][0]) == int(shipchooseid[j+1][0])-1 and int(shipchooseid[j][1]) == int(shipchooseid[j+1][1]):
                    pass
                
                #Not horizontal - continue checking for vertical
                else:
                    ori= False
                    break
                    #break out for the for loop (which is checking for horizontal)
                    
            #if after the checking of horizontal, ori still remains True, then placement is HORIZONTAL
            if ori:
                return ori
            
            #vertical  
            ori = True
            for k in range(len(shipchooseid)-1):
                if int(shipchooseid[k][1]) == int(shipchooseid[k+1][1])-1 and int(shipchooseid[k][0]) == int(shipchooseid[k+1][0]):
                    pass
                else:
                    pop = Popup(title='Wrong Placement', content=Label(text='Ships can only be placed horizontally or vertically.\nShips cannot be placed diagonally.'), size_hint=(None,None),size=(400,400))
                    pop.open()
                    ori = False
                    break
            return ori
                    
    #Boolean function
    #check availability
    def checkavail(self, length):  
        #gets name of ship using the length
        ship_name = nameship[length]
        if self.shipavb[ship_name] >= 1:
            self.shipavb[ship_name] = self.shipavb[ship_name]-1
            self.ids.labelupdate.text = "{}\n{}\n{}\n{}".format(self.shipavb["Battleship(4)"],self.shipavb['Cruiser(3)'],self.shipavb['Destroyer(2)'],self.shipavb['Submarine(1)'])
            return True
        else:
            pop = Popup(title='Not Available', content=Label(text='All {} has been placed'.format(ship_name.rstrip("()4321"))), size_hint=(None,None),size=(400,400))
            pop.open()
            return False
            
# End of Helper functions for checkship --------------------------------------------------------------------------------------------------    
        
    # invoked when the last ship is placed    
    def nextscreen(self,instance):
        # creates the enemy (PC) ships
        self.eneship = self.create_ene_ship()
        sm.current = "level"
        
# Helper functions for creating enemy ships ------------------------------------------------------------------------------------------
    def create_ene_ship(self):     
        for number,size in enumerate([4,3,2,1],1):
            for times in range(number):
                self.create_one_ene_ship(size)
        print("finaleneship",self.finalenship,"\n","availid",self.availid)
    
     
    def create_one_ene_ship(self,a):
        met = False
        while not met:
            basis = random.choice(self.availid)
            direc = random.choice([1,-1])
            size = random.choice([a,-a])
            for combi in [[size,direc],[-size,direc], [size,-direc],[-size,-direc]]:
                sizee,direcc = combi
                print("combi",combi)
                oneship = self.createoneship(basis,direcc,sizee)
                if oneship != False:
                    if self.ckavail(oneship) == False:
                        oneship = False
                if oneship != False:
                    break
            if oneship == False:
                met = False
                #print("try",oneship)
            else:
                met = True
                print("final",oneship)
                surrlist = checksurr(oneship)
                for usedunit in oneship:
                    self.availid.remove(usedunit)
                for usedunit in surrlist:
                    if usedunit in self.availid:
                        self.availid.remove(usedunit)
                ship_name = nameship[abs(a)]
                newval = self.finalenship[ship_name]
                shipnsurr = [oneship,surrlist]
                newval.append(shipnsurr)
                self.finalenship[ship_name] = newval
            #print("AVAILID",availid)
            
    def ckavail(self,oneship):
        for i in oneship:
            if i not in self.availid:
                return False
    
    def createoneship(self,basis,direcc, sizee):
        if direcc == 1:
            oneship = self.vertship(basis,sizee)
        else:
            oneship = self.horiship(basis,sizee)
        return oneship 
                
    def horiship(self,coord,size):
        final = []
        if size < 0:
            step = [coord[1]-x for x in range(-size)]
        else:
            step = [coord[1]+x for x in range(size)]
        for i in step:
            if i <= 0 or i >= 11:
                print(i,final)
                return False
            else:
                final.append([coord[0],i])
        final.sort()
        return final
    
    def vertship(self, coord,size):
        final = []
        if size < 0:
            step = [coord[0]-x for x in range(-size)]
        else:
            step = [coord[0]+x for x in range(size)]
        for i in step:
            if i <=0 or i >= 11:
                print(i, final)
                return False
            else:
                final.append([i, coord[1]])
        final.sort()
        return final            
# End of Helper functions for creating enemy ships ------------------------------------------------------------------------------------------

class Levelscreen(Screen):
    level = ""
    leveloptions = ["Level 1","Level 2","Level 3"]
    def on_pre_enter(self):
        for i in range(len(self.leveloptions)):
            self.btn = Button(text=self.leveloptions[i],height = 0.001, width = 0.001)
            self.btn.bind(on_press=self.nextscreen)
            self.ids.levelgrid.add_widget(self.btn)
        
    def nextscreen(self, instance):
        self.level = instance.text
        sm.current = "game"

class Gamescreen(Screen):
    myshipdict = {}
    eneshipdict = {}
    myshipboard = {'Battleship(4)': 1, 'Cruiser(3)': 2, 'Destroyer(2)': 3, 'Submarine(1)': 4}
    eneshipboard = {'Battleship(4)': 1, 'Cruiser(3)': 2, 'Destroyer(2)': 3, 'Submarine(1)': 4}
    eneavailunits = [[i,j] for i in range(1,11) for j in range(1,11)]
    enehitlist = {'hit':[],'dir':[], 'next':[]}
    
    def on_pre_enter(self):
        
        self.myship = self.manager.get_screen('setup').finalship
        self.eneship = self.manager.get_screen('setup').finalenship
        self.level = self.manager.get_screen('level').level
        print("chosenships",self.manager.get_screen('setup').finalship)
        print("enemyships",self.manager.get_screen('setup').finalenship)
        print("level: ",self.manager.get_screen('level').level)

        
        for i in range(100):
            self.btn = ToggleButton(id=numid[i], height = 0.001, width = 0.001)
            self.btn.bind(on_press=self.update)
            self.ids.enemyborder.add_widget(self.btn)
            self.eneshipdict[self.btn.id] = self.btn
        
        for i in range(100):
            self.btn = ToggleButton(id=numid[i], height = 0.001, width = 0.001)
            self.btn.background_disabled_normal = self.btn.background_normal
            self.ids.yourborder.add_widget(self.btn)
            self.myshipdict[self.btn.id] = self.btn
            self.btn.disabled = True

    # when you click a togglebutton (on the enemy border - RHS grid)
    def update(self, instance):
        print("update function")




# Kivy setup --------------------------------------------------------------------------------------------------------------------------
sm = ScreenManager()
sm.add_widget(Setup(name="setup"))
sm.add_widget(Levelscreen(name="level"))
sm.add_widget(Gamescreen(name="game"))

class MultiApp(App):
    def build(self):
        Clock.schedule_once(self.set_background, 0)        
        return sm
    def set_background(self, *args):
        self.root_window.bind(size=self.do_resize)
        #print(self.root_window.size)
        with self.root_window.canvas.before:
            self.bg = Rectangle(source='ocean.jpg', pos=(0,0), size=(self.root_window.size))

    def do_resize(self, *args):
        self.bg.size = self.root_window.size

if __name__ == "__main__":
    MultiApp().run()
    