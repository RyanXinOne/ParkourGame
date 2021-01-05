# Parkour Game Project Mannual

General
---
+ Developer: Yanze Xin s19236yx
+ Test environment: Python 3.8
+ Developed at: Windows10
+ Designed frame rate: 65 fps

All codes have been formated to follow the Python *PEP8* specification.
***

## Before Start
This game would run in full screen by default.
+ Recommended resolution: ***1600x900***

You will have an option to play in window mode with mismatched screen resolution.
***

## Start Game
Under the project root directory `Parkour/`, run file `startGame.py` using Python3.
***

## How to play
Under *normal* difficulty level, press **Space** key to jump by default. Try to avoid all obstacles encountered and run as far as you can.

The *hard* level requires player to control two independent characters.
***

## Default Key Settings
| Operation | Default Key |
| :-: | :-: |
| Character 1 jump | `<Space>` |
| Character 2 jump | `<Up>` |
| Pause / Resume | `<ESC>` |
| Cheat Code | `<r>` |
| Boss Key | `<b>` |

***Note:*** All key settings can be customized in the game and will be saved in the local file `data/setting.pickle`.
***

## Leaderboard
Seperate leaderboards are set for the level *normal* and *hard*. They are stored in the local file `data/rank.pickle`. Top 10 records would be displayed in the game.
***

## Save/Load Feature
You can save your game progress any time in the *pause* menu and load it from main menu to resume playing next time. The record will save in the local file `data/save.pickle`.

***Note:*** Each game progress has a **unique** game ID. If the game is over, the corresponding saved record will be **deleted**. This is to prevent achieving unlimited scores with save/load function.
***

## Cheat Code
If cheating was enabled, you can jump against the laws of physics, which means you can make your character rocket to the sky to avoid all obstacles.
***

## Boss Key
### Hide
If *Boss Key* was pressed, the game would be automatically paused and the window would **completely hide** (become a transparent window). In the meantime, the title and the icon of the game would pretend to be a *word* document, so does the preview of the window. (The icon camouflage only works under *Windows*, never mind.)

### Recover
You should press *Boss Key* again to make the window visible to you.

If it fails to recover, you may firstly need to **get focus** of the window by clicking the game process (probably an artificial *word* document) in your taskbar, even if nothing happens. Then try to press *Boss Key* again.
***

## Media Resource Copyright
> All images come from <https://www.kenney.nl/assets>.  
> Created/distributed by [Kenney](www.kenney.nl).  
> License: (Creative Commons Zero, CC0)  
> <http://creativecommons.org/publicdomain/zero/1.0/>  
> "This content is free to use in personal, educational and commercial projects."  
***
