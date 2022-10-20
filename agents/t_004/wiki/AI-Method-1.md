# AI Method 1 - Minimax

This section describes our Reversi AI approach based on the Minimax Algorithm with alpha-beta pruning to avoid 
unnecessary calculations, while focusing on the heuristics being used that made meaningful improvements in various
aspects.


# Table of Contents
- [Motivation](#motivation)
- [Application](#application)
- [Solved challenges](#solved-challenges)
- [Evolution and Experiments](#evolution-and-experiments)
- [Trade-offs](#trade-offs)
  * [Strengths](#strengths)
  * [Limitations](#limitations)
- [Future improvements](#future-improvements)

## Motivation  
It is kinda difficult to effectively utilise the traditional classical planning search algorithms at the first glance 
for this game due to its non-determinism (i.e., what the opponent will play in the next turn is not guaranteed), while 
the state space being super large, therefore measuring heuristics of a state could be a useful approximation of the goal 
states. Just like many decent human players would do, by measuring heuristics we are kinda like simulating what a human 
would think of a game state that to what degree that state has a better chance of winning than going for other actions.
Since Reversi is a zero-sum two player game, meaning if one party gains certain advantages, then the other part loses
them, therefore maximising a player's chances of wining minimises the other, and vice versa. This is why Minimax
becomes useful. As long as the heuristics are meaningful that measure domain knowledge in a reasonable degree, while
Minimax algorithm discovers the possibilities of all states within a pre-defined depth, the AI is expected to make moves
towards the most promising state to maximise its winning rate based on the measurement. The alpha-beta pruning technique 
additionally, is used to strive on making the agent return the action as soon as possible within the given time limit 
(1 second), therefore potentially allows us to increase the depth of the Minimax algorithm that makes the agent more 
informed about the available actions.

[Back to top](#table-of-contents)

## Application  
As mentioned previously, the program consists of mainly three parts, the Minimax algorithm, the alpha-beta pruning
technique and the heuristics. While Minimax with alpha-beta pruning can be used in many zero-sum games, the heuristics
are the main components that determine the overall performance of the AI towards a particular game problem, and are 
typically comprised of the relevant domain knowledge. 

The state defined in the algorithm remains the same as the one passed into the selectAction function as a parameter.
Original game functions such as getLegalActions are also used for the particular purposes, although they are slightly
modified in our own version for time efficiency. There's no explicit notion of a goal state in the algorithm, instead 
we use heuristics to measure the chances of winning as previously mentioned if a particular state is reached in the
future, however it is worth mentioning, while we dynamically change the weight for each heuristic component, at the 
very last move we measure the heuristic value purely based on the number of our pieces on board that matches what 
we would consider a win or loss for a typical goal state, the detail of weights is discussed later. The heuristic values
are purely measured on the deepest states bounded by the pre-defined depth, then the values are back-propagated to the parents
while their parents select the maximum or minimum one depending on whether the corresponding layer represents our turn
or the opponent's. The immediate action with the maximum heuristic value will be selected finally.

The depth we used for this Minimax program has been mainly 3 all the time throughout the development and was still 
available for our final version, that our program did not experience significant amount of timeout after our heuristic 
calculations were finalised. Going deeper such as depth=4 would result in timeout on server as we experienced before,
while shallower depth like depth=2 has indicated a lower performance based on experiments discussed later than depth=3 
due to its relative lack of information.

Our heuristic function evaluates the following components which are aggregated together to indicate the overall 
value of the evaluated state:
1. **Corner Heuristic:**

In the game state being evaluated, the number of corner squares we occupied V.S. the number of corner squares our 
opponent occupied. Measured in 25 * (our occupied corners - opponent's occupied corners), where 25 is a 'first layer
weight', that will be combined with the dynamic weight function later. It is worth mentioning here that the weight values
don't really matter as far as we discovered, but the relevance among all measurements. That is, for example, they can
all be measured within -100 and 100 or -1 and 1 that doesn't matter as long as all measurements remain consistent. For
our calculation, we tend to bound the values somewhere near -100 and 100 before assigning them another layer of weights,
exceptions apply to some other components discussed later.

Reason: Capturing corners is very important in most cases that usually significantly determines win or loss, since corners
captured will always be stable and makes the neighboring squares stable as well, while giving many opportunities in three
directions. The more corners captured, the more likely it is to win for that party in many cases.

2. **Piece Count Heuristic:**

In the game state being evaluated, the number of squares we occupied V.S. the number of squares our opponent occupied,
namely comparing the current score for us and for our opponents. This is measured in 100 * (our score - opponent score) 
/ (our score + opponent score), where 100 is also a 'first layer weight', and the latter calculation bounds the total 
value between -100 and 100.

Reason: It is how the win/loss is measured at the end, although in the early game we don't actually want to capture
too many pieces according to professional advices online and experiments, as it will give opponents more actions to
take that gains advantages over us. However,we do want to focus on capture as many as possible in the late game, and
that's why we enabled dynamic weights to shift focus just like a human would do based on the board time.

3. **Mobility Heuristic:**

Throughout the path (chain of actions) down to the game state being evaluated, the amount of actions we could take
in total V.S. the amount of actions our opponent could take in total. Measured in 100 * (our mobility - opponent mobility) 
/ (our mobility + opponent mobility) where mobility refers to amount of actions one could take throughout. 

Reason: The more actions we have, the more opportunities we have, and vice versa, such that in the best case limit
the opponent to choose from only bad moves that no matter what facilitate our advantages later.

4. **Stability Heuristic:**

Stability refers to the stable pieces which can't be flipped by any means. In the game state being evaluated, 
the number of our stable pieces V.S. the number of opponent's stable pieces. The calculation starts from the four 
corners, and spread around to the centre, since only corners are guaranteed to be stable at the first glance, while 
other squares depend on whether their neighbor squares from four different sets of directions are defined as stable. 
In short, stability calculation is executed two times in total for both us and our opponent, while each time stable 
pieces are added into a processing list starting from the corners, then we pop a stable piece each round to assess its 
neighbors until the calculation terminates. All stable pieces are guaranteed to be counted while all non-stable pieces 
are not, in our calculation. The final stability heuristic value is measured in our stability - opponent stability, 
with no 'first layer weight', since this value itself ranges from -64 and 64, the outer weight assigned later will be 
adjusted however to reflect its importance. Another worth mentioning point is, if no corner is occupied by one party, 
the stability value for that party is also 0.

Reason: Stable pieces cannot be flipped, therefore the more stable pieces we have the less pieces the opponent can
gain from, and vice versa.

5. **Static Weights Heuristic:**

In the game state being evaluated, our total static weights V.S. our opponent total static weights, based on the 
pre-defined static weights for each square occupied by the corresponding party and then add up together. The pre-defined
static weights we utilised captures the importance of each square in a general sense, and is used to guide our AI especially
in the early game. This heuristic value is measured in our total static weights - opponent total static weights.

Reason: Gives the AI some sort of indicator on whether placing a piece on a particular square is a good move, although
it is static that does not change throughout the game, which seems less effective, it does help the AI in terms of avoiding
bad moves in the early game especially squares that gives opponent opportunities to gain the corners.

6. **Frontier Heuristic:**

Frontier refers to a piece which its neighborhood contains empty square(s) (i.e., at least one of its 8 neighbor squares
is empty), that typically refers to pieces that give the other party potential opportunities to flip or place pieces. For
this heuristic, we measure our total number of empty square neighbors of all frontiers V.S. opponent's in the game state
being evaluated, with duplicates. It is calculated in 100 * (opponent frontier - our frontier) / (our frontier + opponent
frontier) where 100 is the 'first layer weight', and the latter value is bounded within -1 and 1.

Reason: The more frontiers we have, the more actions our opponent can take that can potentially limit us to only bad
moves. Striving on keeping our pieces surrounded provides potential opportunities later while limits the opponent's 
actions, as proven by professional advices and experiments.

More details about the characteristics and performance measurements are discussed later.

The heuristic values are summed up together at the end after their corresponding weights at the corresponding board time
(number of pieces on board) have been applied. The weights are designed for the following different phases:
1. **Early game (before 28 pieces on board):**

In the early phases, we don't really want too many pieces and probably 
counter intuitively we even want as fewer pieces as possible sometimes, because more pieces on board meaning more actions
for opponent that they have more opportunities to limit our moves, therefore we give a relatively very small weight and
even a negative weight for the piece count heuristic. While it is worth noting that, in the early game, the corner and 
stability heuristics are usually not relevant as in many cases no corner would be captured by either party, therefore
the other heuristics have become the dominators in the early game, namely the mobility, static weights and frontier. Although
in this case, we still value the corner and stability heuristics much higher than the others to encourage our agent capture
them if such cases happen even though it's rare. The weight values are designed based on observations during experiments, 
however our design intention is to make our AI pay more attention on the frontiers and static weights, while frontiers 
gives us more opportunities and limit the opponent's, the static weights avoid our agent place pieces especially around 
the corner(s) that allow the opponent to capture them later, and the mobility plays a certain less important role, 
typically when two states with similar frontier and static weights, that the mobility value could be the decision maker 
in that case.


2. **Middle game (after 27 pieces and before 57 pieces on board):**

In the middle game, corners are more likely to be captured
than in the early rounds. The weight for corner heuristic is designed to be much larger than the others to allow agent
take the corners as much as possible in most cases, while the weight for stability is also high, they won't conflict each
other as taking a corner is also taking a stable square. We slightly increased the weight for frontier as it becomes more
important usually than the others.


3. **Late game (after 56 pieces on board):** 

Each board time is measured individually however they are very similar and
share the same design principles, that is encourages getting as many pieces as possible while reducing the power of
other heuristics like mobility, static weights and frontier, as the opportunities they provide become meaningless as
the game approaches the end.

[Back to top](#table-of-contents)

## Solved Challenges
This means that the difficulties (challenges) you were facing when coding and how you solve them.

There are various challenges we encountered throughout the development of this AI approach, as discuss in the following:
1. **Lack of understanding towards the heuristic measurement**

2. 


3. **##### Measuring weights for each heuristic components**



[Back to top](#table-of-contents)

## Evolution and Experiments

[Back to top](#table-of-contents)

## Trade-offs  
### *Strengths*  


### *Limitations*

[Back to top](#table-of-contents)

## Future improvements  
stability and frontier calculation
mobility isn't explicitly useful
consider anchor play
consider opening play
other heuristics in the book
[Back to top](#table-of-contents)
