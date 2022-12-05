# Score-Counter-Game
***Description:*** A console application focused on using many of Python's features mainly from standard library but also from the most basic modules. 
User in the game earns points for playing in four mini-games and at the end user can see its score and place at the leader board. Whole activity is saving into logs logs.txt file. A plan to expand this project in the future is to use curses module to create good looking terminal.
***Whole project and idea for it is totally my authorship!***

## Required
- Minimum Python 3.10
- Good to have pycharm

## What I learned
- How to plan and creating project from scratch and expand existing projects with new features
- How to use my knowledge of python and programming into actually creating project
- Good division project into separated files which works with each other
- Put most code into classes and functions (OOP approach)
- Get in the habit of writing code frequently and writing it clean with descriptive comments
- Working with Git (aspecially into pycharm)

### Used technologies
`Python 3.10`, `Git`

## Run code in GitPod
<a href="https://gitpod.io/#https://github.com/JakubSzuber/Score-Counter-Game/blob/master/main.py" rel="nofollow"><img src="https://camo.githubusercontent.com/76e60919474807718793857d8eb615e7a50b18b04050577e5a35c19421f260a3/68747470733a2f2f676974706f642e696f2f627574746f6e2f6f70656e2d696e2d676974706f642e737667" alt="Open in Gitpod" data-canonical-src="https://gitpod.io/button/open-in-gitpod.svg" style="max-width: 100%;"></a>

##  Flowchart for Score-Counter-Game
```mermaid
flowchart TD
  A(Start) --> B[Execute start window];
  B --> C[Execute number quessing mini-game];
  C --> D[Execute card game];
  D --> E[Execute memory mini-game];
  E --> F[Execute quiz mini-game];
  F --> G[Execute end window];
  G --> H{Do user want to see leader board?};
  H -- Yes --> I{Output leader board};
  I --> J;
  H -- No --> J(End);
  J --> B;
```
