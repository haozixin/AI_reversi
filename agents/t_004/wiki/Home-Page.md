# UoM COMP90054 Contest Project

## Video Link
https://www.youtube.com/watch?v=4UrY6XuXeaA

## Team Members
* Zixin Hao - zixhao1@student.unimelb.edu.au - 1309180
* Yinghua Zhou - yinghuaz@student.unimelb.edu.au - 1308266

## Introduction
In this project, our team "Plan for Plan" implemented two different AI agents for playing the Reversi/Othello game. 
The first method to describe, and the final method we decided to present is based on the **minimax algorithm(Alpha-Beta Pruning)**, 
which is a popular AI approach for zero-sum games, that explores all possible actions in different turns of the corresponding 
player within a pre-defined depth, with the value of a state measured in heuristics based on domain knowledge, while alpha-beta 
pruning technique is used to avoid redundant calculations. The second method is based on the **Monte Carlo Tree Search (MCTS)**, 
in which our version basically takes elements from the Minimax algorithm, but focuses on running simulations instead of
heuristics. The implementation of two AI approaches are under the folder `agents.t_004`. 
Namely, `myTeam.py` for the Minimax approach, and `myTeam2.py` for the MCTS approach.

This wiki presents the details regarding the two methods and the relevant experiments we did. The contents are categorised 4 sections:
1. [Home Page]()
2. [Approach One](AI-Method-1)
3. [Approach Two](AI-Method-2)
4. [Problem Analysis and Conclusions](Problem-Analysis-and-Conclusions.md)

The details about the two AI approaches we discovered and implemented are included in Section 2 and Section 3 respectively.
The content includes our design decisions and strategies used, challenges we faced, evolution and experiments of the two
approaches respectively (namely how our AI agent evolved and the results for the experiments we did with analysis), 
the strengths and weaknesses of the specific approach, with lastly the possible future improvements.

We will present on which approach we decided to use as our final agent with the reasons outlined in the *Problem Analysis and Conclusions* Section,
with some relative comments and discussions. We will finally conclude our work and learnings at the end of the section.