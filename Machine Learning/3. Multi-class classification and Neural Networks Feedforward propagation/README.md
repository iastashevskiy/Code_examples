Project implements recognition of handwritten digits from 0 to 9 using logistic regression and neural networks. Dataset 
is obtained from ex3data1.mat file that contains 5000 training examples of handwritten digits.Each training
example is a 20 pixel by 20 pixel grayscale image of the digit. Each pixel is represented by a 
floating point number indicating the grayscale intensity at that location. The 20 by 20 grid of pixels is unrolled into a 400-dimensional
vector.

ex3.m master file randomly selects 100 rows and passes those rows to the displayData function.
lrCostFunction.m calculates vectorized regularized cost function and gradient, after that one-vs-all classification is implemented in 
oneVsAll.m. One vs all classifier is used in predictOneVsAll.m to predict a digit contained in a given image.

Second part use a neural network approach to perform this task. Master file is ex3_nn.m. Neural network used has 3 layers - an input layer, a
hidden layer and an output layer.Network parameters were provided by Stanford university in ex3weights.mat and will be
loaded by ex3 nn.m into Theta1 and Theta2.
Feedforward propagation is implemented in predict.m file.
