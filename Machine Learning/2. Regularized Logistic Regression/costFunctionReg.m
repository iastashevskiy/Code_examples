function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

cst = 0;
summ = 0;
for i = 1:m
  z = theta'*X(i,:)';
  cst = -y(i)*log(sigmoid(z))-(1-y(i))*log(1-sigmoid(z));
  summ = summ + cst;
endfor
J_unreg = summ/m;

summ_theta = 0;
for i = 2: length(theta)
  summ_theta = summ_theta + theta(i)^2;
endfor
regularization_parameter = lambda*summ_theta/(2*m);

J = J_unreg + regularization_parameter;


% =============================================================
summ = 0;
  for i = 1:m
    z = theta'*X(i,:)';
    summ = summ + (sigmoid(z) - y(i))*X(i,1);
  endfor
grad(1) = summ/m;

for j = 2:size(theta)
  summ = 0;
  for i = 1:m
    z = theta'*X(i,:)';
    summ = summ + (sigmoid(z) - y(i))*X(i,j);
  endfor
  grad(j) = summ/m + lambda*theta(j)/m;

endfor



end
