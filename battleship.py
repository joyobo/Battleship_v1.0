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
    # dictionary list of id for all the buttons created on both grids
    myshipdict = {}
    eneshipdict = {}
    # boards to keep track of what is available - normal buttons
    myshipboard = {'Battleship(4)': 1, 'Cruiser(3)': 2, 'Destroyer(2)': 3, 'Submarine(1)': 4}
    eneshipboard = {'Battleship(4)': 1, 'Cruiser(3)': 2, 'Destroyer(2)': 3, 'Submarine(1)': 4}
    
    # PC memory
    eneavailunits = [[i,j] for i in range(1,11) for j in range(1,11)]
    enehitlist = {'hit':[],'dir':[],'next':[]} #for level 2 and 3
    # dir: a list with the confirmed/currently using direction at index 0
    # next (the next move that the PC has calculated): when there is a hit (unit in 'hit' list); the next pc move is the unit in this next list 
    # hit: a list with hits (that hasnt result in a FULL sink)
    
    def on_pre_enter(self):
        
        self.myship = self.manager.get_screen('setup').finalship
        self.eneship = self.manager.get_screen('setup').finalenship
        self.level = self.manager.get_screen('level').level
        print("chosenships",self.manager.get_screen('setup').finalship)
        print("enemyships",self.manager.get_screen('setup').finalenship)
        print("level: ",self.manager.get_screen('level').level)

        
        for i in range(100):
            self.btn = ToggleButton(id=numid[i], height = 0.001, width = 0.001)
            self.btn.bind(on_press=self.levelfunction)
            self.ids.enemyborder.add_widget(self.btn)
            self.eneshipdict[self.btn.id] = self.btn
        
        for i in range(100):
            self.btn = ToggleButton(id=numid[i], height = 0.001, width = 0.001)
            self.btn.background_disabled_normal = self.btn.background_normal
            self.ids.yourborder.add_widget(self.btn)
            self.myshipdict[self.btn.id] = self.btn
            self.btn.disabled = True

    # when you click a togglebutton (on the enemy border - RHS grid)
    def levelfunction(self, instance):
        # my turn
        print("processing my turn")
        #on_press meaning that the togglebutton is clicked already and state changes from 'normal' to 'down'
        #button is SELECTED
        if instance.state == 'down':
            print(instance.id,type(instance.id))
            r,c = instance.id.strip("[]'").split(",") 
            unit = [int(r),int(c)]
            hit = self.checkhit(unit,self.eneship,self.eneshipdict,self.eneshipboard,self.ids.eneshipupdate)
            if hit == None:
                instance.disabled = True
        # else if a down button is clicked - nothing happens
        
        # PC turn - different in terms of level chosen
        print("processing PC turn")
        if self.level == "Level 1":
            self.level1()
            
        elif self.level == "Level 2":
            self.level2()
        else: #level 3
            self.level3()
            
    # processing PC unit ---------------------------------------------------------------------------------------
    def level1(self):
        # PC gets a random unit to choose
        pcunit = random.choice(self.eneavailunits)
        print("level selected: ", self.level,"; pcunit: ",pcunit)    
        hit = self.checkhit(pcunit,self.myship,self.myshipdict,self.myshipboard,self.ids.myshipupdate)
                       
    def level2(self):
        # PC checks if there is no previous hits
        hitlist = self.enehitlist.get('hit')
        if hitlist == []: 
            pcunit = random.choice(self.eneavailunits)
        else:
            pcunit = self.enehitlist.get('next')
        print("level selected: ", self.level,"; pcunit: ",pcunit)    
        hit = self.checkhit(pcunit,self.myship,self.myshipdict,self.myshipboard,self.ids.myshipupdate)
                
        # never hit
        if hit == None:
            if len(self.enehitlist.get('hit')) == 1: #dir not cfm
                self.returnnextunit(False)
            elif len(self.enehitlist.get('hit')) >= 2: #dir cfm
                self.returnnextunit(True)
                
        # hit full ship
        elif hit == True:
            print("full hit")
            self.enehitlist['hit'] = []
            self.enehitlist['dir'] = []
            self.enehitlist['next'] = []
        
        # hit
        elif hit == False:
            print("hit")
            # update the hit list in enehitlist with the hit unit
            hitlist = self.enehitlist.get('hit')
            hitlist.append(pcunit)
            hitlist.sort()
            self.enehitlist['hit'] = hitlist
            
            # first hit & dir not cfm
            if len(self.enehitlist.get('hit')) == 1:
                print("pc hit once", pcunit)
                self.returnnextunit(False) 
            
            # dir cfm
            elif len(self.enehitlist.get('hit')) >= 2:
                self.returnnextunit(True)
        
    def level3(self):
        #diff from level 2: certain units where there isnt a ship logically- > PC wont choose it
        # on every PC turn, check if a certain length of ship can fit
        print("level selected: ", self.level)
         # PC checks if there is no previous hits
        hitlist = self.enehitlist.get('hit')
        if hitlist == []: 
            if self.myshipboard['Submarine(1)'] == 0:
                self.update_ene_avail(1)
                print('update: all 1 units sank',self.eneavailunits)
                
                if self.myshipboard['Destroyer(2)'] == 0:
                    self.update_ene_avail(2)
                    print("update: all 1 and 2 units sank",self.eneavailunits)
                    
                    if self.myshipboard['Cruiser(3)']==0:
                        self.update_ene_avail(3)
                        print("update: all 1 and 2 and 3 units sank",self.eneavailunits)
            print("eneavailunits/units that PC can choose from: ",self.eneavailunits)
            # FOR TESTING PURPOSES -------------------------------
#            if [1,1] in self.eneavailunits:
#                pcunit = [1,1]
#            elif [10,1] in self.eneavailunits:
#                pcunit = [10,1]
#            elif [10,10] in self.eneavailunits:
#                pcunit = [10,10]
#            elif [1,10] in self.eneavailunits:
#                pcunit = [1,10]
#            else:
#                pcunit = random.choice(self.eneavailunits)
            # -----------------------------------------------------
            pcunit = random.choice(self.eneavailunits)

        else:
            pcunit = self.enehitlist.get('next')

        print("level selected: ", self.level,"; pcunit: ",pcunit)    
        hit = self.checkhit(pcunit,self.myship,self.myshipdict,self.myshipboard,self.ids.myshipupdate)
                
        # never hit
        if hit == None:
            if len(self.enehitlist.get('hit')) == 1: #dir not cfm
                self.returnnextunit(False)
            elif len(self.enehitlist.get('hit')) >= 2: #dir cfm
                self.returnnextunit(True)
                
        # hit full ship
        elif hit == True:
            print("full hit")
            self.enehitlist['hit'] = []
            self.enehitlist['dir'] = []
            self.enehitlist['next'] = []
        
        # hit
        elif hit == False:
            print("hit")
            # update the hit list in enehitlist with the hit unit
            hitlist = self.enehitlist.get('hit')
            hitlist.append(pcunit)
            hitlist.sort()
            self.enehitlist['hit'] = hitlist
            
            # first hit & dir not cfm
            if len(self.enehitlist.get('hit')) == 1:
                print("pc hit once", pcunit)
                self.returnnextunit(False) 
            
            # dir cfm
            elif len(self.enehitlist.get('hit')) >= 2:
                self.returnnextunit(True)



    # unit - the selected unit to be checked if it is a hit
    # shiplist - list of the chosen ships 
    # dictt - dictionary list of id for all the buttons created on both grids
    # board - to keep track of what is available - normal buttons
    # label - id of the number of ships left
    # returns boolean - True: full hit; False: single hit; None: no hit
    # additional - for PC turn: full/single hit-> will remove pcunit from enemy available options list; full hit -> remove surr blocks
    def checkhit(self,unit,shiplist,dictt,board,label):
        for key,val in shiplist.items():
            if val:
                for num in val:
                    #unit is a hit
                    if unit in num[0]:
                        num[0].remove(unit)
                        dictt.get(str(unit)).state = 'down'
                        dictt.get(str(unit)).add_widget(Image(source = 'ship_unit.png', size = (dictt.get(str(unit)).width, dictt.get(str(unit)).height), pos = dictt.get(str(unit)).pos))
                        dictt.get(str(unit)).disabled = True
                        # for pc, need to remove the choice from enemy available options lists
                        if shiplist == self.myship:
                            self.eneavailunits.remove(unit)
                        # if an empty list - full hit
                        if not num[0]:
                            #opening and disabling the surr
                            for everysurr in num[1]:
                                if dictt.get(str(everysurr)).state == 'normal':
                                    dictt.get(str(everysurr)).state = 'down'
                                    dictt.get(str(everysurr)).disabled = True
                                if shiplist == self.myship:
                                    if everysurr in self.eneavailunits:
                                        self.eneavailunits.remove(everysurr)
                                    
                            # reflect on the scoreboard
                            val = board.get(key)
                            newval = val - 1
                            board[key] = newval
                            label.text = "{}\n{}\n{}\n{}".format(board["Battleship(4)"],board['Cruiser(3)'],board['Destroyer(2)'],board['Submarine(1)'])
                            

                            #check for WIN
                            if self.myshipboard["Battleship(4)"] == 0 and self.myshipboard['Cruiser(3)'] == 0 and self.myshipboard['Destroyer(2)'] == 0 and self.myshipboard['Submarine(1)'] == 0:
                                self.winbtn = Button(height = 1, width = 1,background_color = [0,0,0,0],text="PC wins!",font_size=400)
                                self.ids.overallscreen.add_widget(self.winbtn)
                                self.winbtn.disabled = True
                            if self.eneshipboard['Cruiser(3)'] == 0 and self.eneshipboard['Destroyer(2)'] == 0 and self.eneshipboard['Submarine(1)'] == 0:
                                self.winbtn = Button(height = 1, width = 1,background_color = [0,0,0,0],text="YOU win!",font_size=400)
                                self.ids.overallscreen.add_widget(self.winbtn)
                                self.winbtn.disabled = True
                            return True
                        return False
                    
        # unit is not a hit
        if shiplist == self.myship:
            self.eneavailunits.remove(unit)
            self.myshipdict.get(str(unit)).state = 'down'

        
# Helper functions ---------------------------------------------------------------------------------------------------------------------
    def returnnextunit(self,direc):
        #direction not cfm
        if direc == False:
            possible = False
            while not possible:
                print("self.enehitlist.get('dir')",self.enehitlist.get('dir'))
                dir_avail = list(set([1,-1,2,-2])-set(self.enehitlist.get('dir')))
                print("dir_avail",dir_avail)
                dir_to_use = random.choice(dir_avail)
                nextunit = self.getnextunit(dir_to_use)
                possible = self.checkpossible(nextunit)
                print('possible',possible)
                dirlist = self.enehitlist.get('dir')
                dirlist.insert(0,dir_to_use)
                self.enehitlist['dir'] = dirlist
        #direction cfm
        elif direc == True:
            dirlist = self.enehitlist.get('dir')
            cfmdir = dirlist[0] #cfm dir at index 0
            dir_to_use = random.choice([cfmdir,-cfmdir])
            nextunit = self.getnextunit(dir_to_use)
            possible = self.checkpossible(nextunit)
            if possible == False:
                nextunit = self.getnextunit(-dir_to_use)
                
        self.enehitlist['next'] = nextunit
        
    def getnextunit(self,dire):
        print(dire)
        hitlist = self.enehitlist.get('hit')
        if dire == 1:
            nextunit = [hitlist[-1][0]+1,hitlist[-1][1]]
        elif dire == -1:
            nextunit = [hitlist[0][0]-1,hitlist[0][1]]
        elif dire == 2:
            nextunit = [hitlist[-1][0],hitlist[-1][1]+1]
        elif dire == -2:
            nextunit = [hitlist[0][0],hitlist[0][1]-1]
        return nextunit
    
    def checkpossible(self,unit):
        if unit not in self.eneavailunits or unit[0] <= 0 or unit[1] <= 0 or unit[0] >= 11 or unit[1] >= 11:
            return False
        else:
            return True
        
    def update_ene_avail(self,num):
        # removing boxes that are single (since all single units are sank)
        if num == 1:
            for ele in self.eneavailunits:
                if [ele[0]+1,ele[1]] not in self.eneavailunits and [ele[0]-1,ele[1]] not in self.eneavailunits and [ele[0],ele[1]+1] not in self.eneavailunits and [ele[0],ele[1]-1] not in self.eneavailunits:
                    print('one',ele)
                    self.eneavailunits.remove(ele) 
        
        # removing boxes that are 2/3 units (since all 2/3 units are sank)
        else:
            self.updatelist(num)

    def updatelist(self,num):
        dictt = self.calculateLength()
        for key,val in dictt.items():
            if key <= num:
                for unit in val:
                    self.eneavailunits.remove(unit)
                    
    def calculateLength(self):
        dictt = {}
        for unit in self.eneavailunits:
            #horizontally
            x = unit[0]+1
            y = unit[1]
            xcount = 1
            # horizontally right
            ele = [x,y]
            while ele in self.eneavailunits:
                x+=1
                xcount+=1
                ele = [x,y]
            # horizontally left
            x = unit[0]-1
            ele = [x,y]
            while ele in self.eneavailunits:
                x-=1
                xcount+=1
                ele = [x,y]
                
            #vertically
            x = unit[0]
            y = unit[1]+1
            ycount = 1
            # vertically right
            ele = [x,y]
            while ele in self.eneavailunits:
                y+=1
                ycount+=1
                ele = [x,y]
            # vertically left
            y = unit[1]-1
            ele = [x,y]
            while ele in self.eneavailunits:
                y-=1
                ycount+=1
                ele = [x,y]
                
            maxlen = max(xcount, ycount)   
            if maxlen in dictt:
                val = dictt[maxlen]
                val.append(unit)
                dictt[maxlen] = val
            else:
                dictt[maxlen] = [unit]    
        return dictt
            
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
    