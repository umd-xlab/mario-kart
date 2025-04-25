%% INTRODUCTION
% TITLE: First derivative calculation
% DESC: This script numerically takes the first derivative of the variable
% passed to it. 

% ACCEPTS: var == array to take derivative. 
%          t == time series
% RETURNS: first_deriv == array: the 2nd order approximation of the first
%                                derivative

function first_deriv = first_derivative(var, t)
    dt = t(2) - t(1);
    for i = 1:length(var)
        if i == 1 
            first_deriv(i) = 1/(2*dt) * (-3*var(i) + 4*var(i+1) - var(i+2));
        elseif i == length(var)
            first_deriv(i) = 1/(2*dt) * (3*var(i) - 4*var(i-1) + var(i-2));
        else
            first_deriv(i) = 1/(2*dt) * (var(i+1) - var(i-1));
        end
    end