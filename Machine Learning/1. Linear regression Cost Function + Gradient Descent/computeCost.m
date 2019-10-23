function J = computeCost(X, y, theta)
%COMPUTECOST Compute cost for linear regression
%   J = COMPUTECOST(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples




% You need to return the following variables correctly 
h = 0;




% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta
%               You should set J to the cost.

for i = 1:m
  predicted_value = theta'*X(i,:)';
  h = h+(predicted_value - y(i))^2;
endfor
J=h/(2*m);



% =========================================================================

end
