%% INTRODUCTION
% TITLE: Second derivative calculation
% DESC: This script numerically takes the second derivative of the variable
% passed to it. 

% ACCEPTS: var == array to take derivative. 
%          t == time series
% RETURNS: second_deriv == array: the 2nd order approximation of the 2nd
%                                 derivative

function second_deriv = second_derivative(var, t)
    dt = t(2) - t(1);
    for i = 1:length(var)
        if i == 1 % left side
            second_deriv(i) = 1/(dt^2) * (2*var(i)-5*var(i+1) + ...
                4*var(i+2) - var(i+3));
        elseif i == length(var) % right side
            second_deriv(i) = 1/(dt^2) * (2*var(i)-5*var(i-1) + ...
                4*var(i-2) - var(i-3));
        else
            second_deriv(i) = 1/(dt^2) * (var(i+1) - 2*var(i) + var(i-1));
        end
        %elseif i == 2 || i == length(var)-1 % 2nd order in center
        %    second_deriv(i) = 1/(dt^2) * (var(i+1) - 2*var(i) + var(i-1));
        %else % 3rd order central just to check and see what's up
        %    second_deriv(i) = 1/(12*dt^2) * (-var(i+2)+16*var(i+1)-30*var(i)+16*var(i-1)-var(i-2));
        %end
    end