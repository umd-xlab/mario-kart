%% INTRODUCTION
% TITLE: Orientation angle calculation
% DESC: This script numerically calculates the body's orientation w.r.t
% its starting value (assuming reference is forward at start)

% ACCEPTS: x_pos == array: x positions to calculate over. 
%          y_pos == array: y position to calculate over
% RETURNS: phi == array: the orientation angle w.r.t the starting
%          orientation, reported in RADIANS

function phi = body_angle(x_pos, y_pos)
    x_start = x_pos(1); y_start = y_pos(1);
    
    % NOTE: by convention, mario starts along the y-axis, so this is
    % treated as the reference axis to start moving along

    for i = 1:length(x_pos)
        delx = x_pos(i) - x_start;
        dely = y_pos(i) - y_start;
        % Handle the 0 case
        if dely == 0
            phi(i) = 0;
        else
            % This is the impact of the note above!
            % We use NEGATIVE y because the orientation of the axis is
            % along the negative y and decreasing when going forward
            % atan2 == atan2(Y,X), but again, we switch conventions
            phi(i) = atan2(delx, -dely); 
        end
    end