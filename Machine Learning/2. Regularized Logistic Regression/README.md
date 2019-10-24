This project implements logistic regression algorithm. Run ex2.m for unregularized logistic regression and ex2_reg.m for 
regularized logistic regression. 

Project for unregularized logistic regression simulates administrator of a university department with a task to determine each applicant's 
chance of admission based on their results on two exams. You have historical data from previous applicants
that you can use as a training set for logistic regression. For each training example, you have the applicant's scores on two exams and 
the admissions decision. 
Dataset obtained from ex2data1.txt file. Cost function is calculated in costFunction.m and then minimized by 
Matlab/Octave built-in function fminunc.

Regularized logistic regression project emulates a product manager of the factory who have the
test results for some microchips on two different tests. From these two tests,
you would like to determine whether the microchips should be accepted or
rejected. Dataset obtained from ex2data2.txt file. Cost function is calculated in costFunctionReg.m and then minimized by 
Matlab/Octave built-in function fminunc.

Sigmoid.m file calculates sigmoid function for logistic regression, predict.m file produces "1" or "0" predictions given a dataset and a learned parameter
vector theta. 
