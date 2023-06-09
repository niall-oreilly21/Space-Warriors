<a name="readme-top"></a>

<div align="center">
  <img src="/src/main/resource/img/icons/logo.png" width="80" height="80">
</div>

<h1 align="center">Space Warriors</h1>
  <p align="center">
    The universe needs your help! Your goal is simple: to navigate through different planets and save each of them; although its probably not as easy as it sounds.
  <br/><br/>
    <a href="https://github.com/niall-oreilly21/PortoMetro"><strong>Explore the project »</strong></a>
    <br />
  </p>
 
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Project Structure
This project includes a game engine and a 2D game in Python using pygame interface. The classes are based on object-oriented principles. The game will incorporate objects from the game engine to define how they behave. The hierarchy of our classes is that objects in the scene are called GameObject and they have a list of Components, for example:
- Animator
- Renderer
- MovementController
- Collider
- RigidBody
- etc.

We also have Manager classes for example:
- SceneManager which defines the active scene e.g., Main Menu, Pause Menu, etc.
- RendererManager to draw all renderers on the screen
- etc.

We use some of the inbuilt functionalities from pygame such as the main game loop and its vector class.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Rules of the Game
+ The main objective of the game is to fight each enemy on each world until all enemies are defeated.

+ Each time the player is hit by an enemy their healthbar decreases.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Camera
+ The Camera is centered on the player at all times when in a level
+ There is also a static camera for menus

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Controls

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Menus
### Main Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/5c39e299-727f-4df7-917e-be90f0d21b32)

### Sound Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/cc887d75-65a1-4820-96bc-b28e74daea61)

### Level Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/780f7fff-89d4-4779-aeb9-adde1cd93dcd)

### Pause Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/a8c492fb-9633-4cc9-905d-745b2b575485)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Key Elements
### Players:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/7a92c9a7-5cb5-4bbd-af2b-c9dd2b2cd5d7)

### Healthbar:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/270576b0-d542-404d-a69d-55bf1845be58)

### Potions:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/fec381cf-a636-42f7-87b3-fdc478a2fd94)

### Pet:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/d08e1dda-05d3-4750-9950-44da76146aa3)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## Levels
There are 3 levels in the game with various difficulty:

### Level 1: Earth - Easy
+ The player has to fight all enemies
+ May find a hidden pet on the island

<br>
<img src="https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/b03a4ea0-6c5d-4f36-8e38-4fa25fa2f831" height = "200"/>
<br><br>

### Level 2: Mars - Medium
+ The player has to fight all enemies
+ Map will be dark and player has a glow ring around them

<br>
<img src="https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/43d7c42e-7741-4c34-9f4c-e56e7dd92f01" height = "200"/>
<br><br>

### Level 3: Saturn - Hard

+ The player has to fight all enemies
+ Includes a boss with gun and bullets

<br>
<img src="https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/ee957d28-0f2a-4929-8dda-c285f9a2d87d" height = "200"/>
<br><br>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

# References to game assets below:


## Sprites References

### Corgi:
https://angryelk.itch.io/animated-corgi-sprite


## Texture References

### Tilesets:
https://itch.io/game-assets/tag-2d

### Game Objects:
https://craftpix.net/categorys/2d-game-objects/


## Map Editor Reference:
https://deepnight.net/tools/rpg-map/

## Audio References

### Music References:

https://mixkit.co/free-sound-effects/game/

https://freesound.org/people/inchadney/sounds/

