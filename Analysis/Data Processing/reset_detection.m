%% INTRODUCTION
% TITLE: Reset detection
% DESC: This script detects if and when an agent resets their position in
% the RL evaluation data

% ACCEPTS: time series data of the x and y positions
% RETURNS: flag == 1 or 0: 1 - a reset occured; 0 - no reset occured
%          idx == int: the time step index when the reset occured, up to
%                      but not including the reset
%          x_trim, y_trim == array: the trimmed list from 0 to idx

function [flag, idx, x_trim, y_trim] = reset_detection(x_pos, y_pos)
    x_start = x_pos(1); y_start = y_pos(1);
    
    % Create a list of displacements from the starting position
    dist = zeros(1,length(x_pos));
    for i = 1:length(x_pos)
        dist(i) = norm([x_start, y_start] - [x_pos(i), y_pos(i)], 2);
    end

    % Now check for the reset!
    i = 2; % Start looping over the list
    while i < length(x_pos)
        % Calculate the displacement from the last position
        displaced = dist(i) - dist(i-1);
        
        % if the change in distance is > 0 and we're back at the start
        % (i,e, dist(i) == 0), then we know we reset
        if abs(displaced) > 0 && dist(i) == 0
            flag = 1;
            break;            
        end
        
        % Continue iteration
        i = i + 1;
    end
    
    % If we reached the end w/o a reset, then set the flag to 0
    if i == length(x_pos)
        flag = 0;
    end
    
    % The last i should be the reset point, so subtract off 1 to have an
    % unreset time series
    if flag == 1
        i = i - 1;
    end
    
    % Trim the series and return!
    idx = i;
    x_trim = x_pos(1:i); y_trim = y_pos(1:i);


