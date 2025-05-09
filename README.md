# The-code-of-DP-and-ADP
I set a environment of the user side battery participate the daily scheduling, Whitch can reduce the cost of the users. The detailed information is shown below:
0.3 <= SOC <= 0.7,   -1 <= Pess <= 1,  initial SOC equals 0.5,  the scheduling horizon T = 6
Every hour demand of user set to 0.3, and the User can buy the power from the grid and use the battery.
the objective is to minimize the cost
the price buy from the gird sets to [0.4,0.5,0.6,0.7,0.8,0.9], if user sell power to the grid, the price sets to 0.5
the basic method of DP and ADP according to the paper:
[1] H. Shuai, J. Fang, X. Ai, J. Wen and H. He, “Optimal Real-Time Operation Strategy for Microgrid: An ADP-Based Stochastic Nonlinear Optimization Approach,” in IEEE Transactions on Sustainable Energy, vol. 10, no. 2, pp. 931-942, April 2019, doi:10.1109/TSTE.2018.2855039.
[2] C. Wang, S. Lei, P. Ju, C. Chen, C. Peng and Y. Hou, "MDP-Based Distribution Network Reconfiguration With Renewable Distributed Generation: Approximate Dynamic Programming Approach," in IEEE Transactions on Smart Grid, vol. 11, no. 4, pp. 3620-3631, July 2020, doi: 10.1109/TSG.2019.2963696.

