function g = sigmoid(z)
%SIGMOID Compute sigmoid function
%   g = SIGMOID(z) computes the sigmoid of z.

% You need to return the following variables correctly 
g = zeros(size(z));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the sigmoid of each value of z (z can be a matrix,
%               vector or scalar).

matrix_size = size(z);
for i = 1:matrix_size(1);
  for j = 1:matrix_size(2);
    E = e^-z(i,j);
    val = 1/(1+E);
    g(i,j) = val;
  endfor
endfor
 




% =============================================================

end
