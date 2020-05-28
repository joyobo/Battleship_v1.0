# Battleship_v1.0
Battleship Game (with Three Difficulty Levels) Using Kivy

Done on 29/5/2020

## How to Play
- Run it and maximise window

Starts with a 10x10 grid boxes for you to place your ships.
<br/><image src="READMEimages/PlaceShips.PNG" width="800"><br/>
The top left corner indicates how many ships are left to be placed.
  
Unsuccessful ship placement results in an error message. One of the following:
<br/><image src="READMEimages/InvalidPlacement.PNG" width="800"><br/>
<br/><image src="READMEimages/InvalidSize.PNG" width="800"><br/>
<br/><image src="READMEimages/NotAvailable.PNG" width="800"><br/>
<br/><image src="READMEimages/WrongPlacement.PNG" width="800"><br/>

Successful placement results in:
<br/><image src="READMEimages/PlacedShip.PNG" width="800"><br/>

When all ships are placed,
<br/><image src="READMEimages/StartBattling.PNG" width="800"><br/>

Then, select level.
<br/><image src="READMEimages/LevelSelect.PNG" width="800"><br/>

Start playing.
<br/><image src="READMEimages/Playing.PNG" width="800"><br/>

You start first. A full hit on a ship uncovers surrounding boxes.
<br/><image src="READMEimages/ShipSinked.PNG" width="800"><br/>

When either won, a win message appears.
<br/><image src="READMEimages/WinMsg.PNG" width="800"><br/>

## Levels
### Level One
PC chooses random units.

### Level Two
PC chooses random units. When a part of a ship is hit, PC will choose the adjacent boxes next.

### Level Three
When a part of a ship is hit, PC will choose the adjacent boxes next. PC won't choose boxes that definitely don't have a ship.
For instance, box at 8 down and 10 across will not be chosen when all submarines (1 unit ships) are sank.
<br/><image src="READMEimages/AllOnesSank.PNG" width="800"><br/>
