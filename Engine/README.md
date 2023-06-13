<a name="readme-top"></a>

![Space Warriors](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/f00e9ee2-1fc8-4297-94b5-6aaa225fd1e8)

  <p align="center">
    The universe needs your help! Your goal is simple: to navigate through different planets and save each of them; although its probably not as easy as it sounds.
  <br/><br/>
    <a href="https://github.com/niall-oreilly21/PortoMetro"><strong>Explore the project »</strong></a>
    <br />
  </p>
 
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 📚&ensp;Project Structure
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

## 📝&ensp;Rules of the Game
+ The main objective of the game is to fight each enemy on each world until all enemies are defeated.

+ Each time the player is hit by an enemy their healthbar decreases.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 📷&ensp;Camera
+ The Camera is centered on the player at all times when in a level
+ There is also a static camera for menus

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🕹&ensp;Controls
<img width="1495" alt="Screenshot 2023-06-10 at 00 58 39" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/46b9a9e5-f786-4b7d-80f0-d5ad83d2d05b">

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🖥&ensp;Menus
### Main Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/5c39e299-727f-4df7-917e-be90f0d21b32)

### Sound Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/cc887d75-65a1-4820-96bc-b28e74daea61)

### Level Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/780f7fff-89d4-4779-aeb9-adde1cd93dcd)

### Pause Menu:
![image](https://github.com/niall-oreilly21/PythonGameEngine/assets/92158821/a8c492fb-9633-4cc9-905d-745b2b575485)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🗝&ensp;Key Elements
### Players:
<img width="107" alt="Screenshot 2023-06-10 at 01 06 15" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/725e571a-eb99-4520-91e1-3582ba993a32"> <img width="107" alt="Screenshot 2023-06-10 at 01 06 38" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/e1eeba4e-e54c-4946-8c87-590d2136d1fb">

### Enemies:
<img width="107" alt="Screenshot 2023-06-10 at 01 13 10" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/26226033-86a5-4548-9128-83fbe95074c3"> <img width="107" alt="Screenshot 2023-06-10 at 01 13 38" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/d5c1e4d9-9ed6-470f-aa14-85cee75179cd"> <img width="107" alt="Screenshot 2023-06-10 at 01 13 58" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/6746c822-e52b-4259-8e60-5cc32d65651b">

### Healthbar:
![health bar](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/a5cd01ca-d647-4ea8-8d1a-8bccb08a3596)

### Potions:
![potion_attack](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/bb53648b-cf55-4dbd-8b5c-db29ab6f8c69) &ensp; ![potion_defense](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/bc0df242-5d2f-40b8-b481-ad41c223d191) &ensp; ![potion_heal](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/9e5471f6-1ea3-4620-94e5-2ab311334eff) &ensp; ![potion_speed](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/1eeffcfe-9290-40ad-8520-5436844412c2) &ensp; ![random](https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/25b5015e-e859-41a2-969f-9d4eff5fc8de)

### Pet:
<img width="104" alt="Screenshot 2023-06-10 at 01 17 36" src="https://github.com/niall-oreilly21/PythonGameEngine/assets/73035581/430c70b1-ee28-4138-bda3-6a074c61de9f">


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 💡&ensp;Levels
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

# References to game assets

## 👾&ensp;Sprites References

### Players & Enemies:
https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator

### Corgi:
https://angryelk.itch.io/animated-corgi-sprite

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🧵&ensp;Texture References

### Tilesets:
https://itch.io/game-assets/tag-2d

### Game Objects:
https://craftpix.net/categorys/2d-game-objects/

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🗺&ensp;Map Editor Reference:
https://deepnight.net/tools/rpg-map/

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🎵&ensp;Audio References

### Music References:

https://mixkit.co/free-sound-effects/game/

https://freesound.org/people/inchadney/sounds/

