function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);

         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
X = [ones(m, 1) X];

for i = 1:m
  Y = zeros(num_labels,1);
  correct_answer = y(i);
  Y(correct_answer) = 1;

    A2 = sigmoid(Theta1*X(i,:)');
    A2 = [1; A2];

    H = sigmoid(Theta2*A2);

    cst = -Y'*log(H)-(1-Y)'*log(1-H);
    J = J+cst;

endfor

J = J/m;

T1 = 0;
for i = 2:input_layer_size+1
  for j = 1:hidden_layer_size
    square_el = Theta1(j,i)^2;
    T1 = T1 + square_el;
  endfor
endfor

T2  = 0;
for i = 2:hidden_layer_size+1
  for j = 1:num_labels
    square_el = Theta2(j,i)^2;
    T2 = T2 + square_el;
  endfor
endfor

R = (T1+T2)*lambda/(2*m);

J = J+R;

%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
  for i = 1:size(Theta2,1)
    line = Theta2(i,:);
    Theta2_no_bias(i,:) = line(2:end);
  endfor
  
   for i = 1:size(Theta1,1)
    line = Theta1(i,:);
    Theta1_no_bias(i,:) = line(2:end);
  endfor

  
for i = 1:m
  Y = zeros(num_labels,1);
  correct_answer = y(i);
  Y(correct_answer) = 1;

  A2 = sigmoid(Theta1*X(i,:)');
  A2 = [1; A2];

  H = sigmoid(Theta2*A2);
  
  Delta3 = H - Y;
  Theta2_grad = Theta2_grad + Delta3*A2';
  
  Delta2 = Theta2_no_bias'*Delta3.*sigmoidGradient(Theta1*X(i,:)');
  Theta1_grad = Theta1_grad + Delta2*X(i,:);
endfor
Theta1_grad = Theta1_grad/m;
Theta2_grad = Theta2_grad/m;

% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%

Theta2_reg = (lambda*Theta2_no_bias)/m;
Theta1_reg = (lambda*Theta1_no_bias)/m;

for i = 1:size(Theta1_grad,1)
  for j = 2:size(Theta1_grad,2)
    Theta1_grad(i,j) = Theta1_grad(i,j) + Theta1_reg(i, j-1);
  endfor
endfor

for i = 1:size(Theta2_grad,1)
  for j = 2:size(Theta2_grad,2)
    Theta2_grad(i,j) = Theta2_grad(i,j) + Theta2_reg(i, j-1);
  endfor
endfor




% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
