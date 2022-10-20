# AI Method 1 - Minimax

This section describes our Reversi AI approach based on the Minimax Algorithm with alpha-beta pruning to avoid 
unnecessary calculations, while focusing on the heuristics being used that made meaningful improvements in various
aspects.


# Table of Contents
- [Motivation](#motivation)
- [Application](#application)
- [Solved challenges](#solved-challenges)
- [Evolution](#evolution)
- [Trade-offs](#trade-offs)
  * [Advantages](#advantages)
  * [Disadvantages](#disadvantages)
- [Future improvements](#future-improvements)

## Motivation  
It is kinda difficult to utilise the traditional classical planning search algorithms at the first glance for this game
due to its non-determinism (i.e., what the opponent will play in the next turn is not guaranteed), while the state
space being super large, therefore measuring heuristics of a state could be a useful approximation of the goal states.
Since Reversi is a zero-sum two player game, meaning if one party gains certain advantages, then the other part loses
them, therefore maximising a player's chances of wining minimises the other, and vice versa. This is why Minimax
becomes useful. As long as the heuristics are meaningful that measure domain knowledge in a reasonable degree, while
Minimax algorithm discovers possibilities of all states within a pre-defined depth, the AI is expected to make moves
towards the most promising state to maximise its winning rate. The alpha-beta pruning technique additionally, is used
to strive on making the agent return the action within the given time limit (1 second), therefore potentially increases
the depth of the Minimax algorithm that makes the agent more informed about the available actions.


[Back to top](#table-of-contents)

## Application  


[Back to top](#table-of-contents)

## Solved Challenges
This means that the difficulties (challenges) you were facing when coding and how you solve them.
[Back to top](#table-of-contents)


## Evolution

[Back to top](#table-of-contents)

## Trade-offs  
### *Advantages*  


### *Disadvantages*

[Back to top](#table-of-contents)

## Future improvements  

[Back to top](#table-of-contents)
