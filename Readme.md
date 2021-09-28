# RegEx to Automate translator


## Contents


Run ./test.sh to get test coverage


Run python3 main.py to start main process


File Automate.py contains main Automate class and some dependent classes


## How it works


### 1) Creating Automate from RegEx which accepts language L
Programm reads symbols from RegEx, creates simple two-nodes automate if it's a letter and connects last two automates else.

### 2) Reversing Automate
Only works if there is exactly one finish. Programm reverses all edges and switches finish and start nodes. Now Automate accepts exactly L reversed

### 3) Determinising

First, programm removes all empty edges (with epsylon) by creating new edges from current node to others which can be reached in 1 letter transition

Second, programm determinises using well-known algorithm

Third, programm deletes all nodes such that it is not possible to reach finish from them and edges which lead to those nodes. This does not change L, but
it is helpful for last step as now it is possible to create a word starting in any node

### 4) Finding longest prefix in L reversed
Programm reads reversed word from input letter by letter and tries to go to the next state in DFA. When it can not do this - it has found the longest suffix in L

