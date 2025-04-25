%% INTRODUCTION
% TITLE: Orientation angle calculation
% DESC: This script numerically calculates the body's orientation w.r.t
% its starting value (assuming reference is forward at start)

% ACCEPTS: x_pos == array: x positions to calculate over. 
%          y_pos == array: y position to calculate over
% RETURNS: phi == array: the orientation angle w.r.t the starting
%          orientation, reported in RADIANS

function phi = body_angle(x_pos, y_pos, vx, vy)
    x_start = mean(x_pos(1:10)); y_start = mean(y_pos(1:10));
    
    % NOTE: by convention, mario starts along the y-axis, so this is
    % treated as the reference axis to start moving along

    % for i = 1:length(x_pos)
    %     delx = x_pos(i) - x_start;
    %     dely = y_pos(i) - y_start;
    %     % Handle the close to zero case to avoid spikes
    %     if abs(dely) < 1 || abs(delx) < 1
    %         phi(i) = 0;
    %     else
    %         % This is the impact of the note above!
    %         % We use NEGATIVE y because the orientation of the axis is
    %         % along the negative y and decreasing when going forward
    %         % atan2 == atan2(Y,X), but again, we switch conventions
    %         phi(i) = atan2(delx, -dely); 
    %     end
    % end

    for i = 1:length(x_pos)
        delx = x_pos(i) - x_start;
        dely = y_pos(i) - y_start;
        % Handle the close to zero case to avoid spikes
        if abs(dely) < 1 || abs(delx) < 1
            phi(i) = 0;
        else
            % This is the impact of the note above!
            % We use NEGATIVE y because the orientation of the axis is
            % along the negative y and decreasing when going forward
            % atan2 == atan2(Y,X), but again, we switch conventions
            phi(i) = atan2(vx(i), -vy(i)); 
        end
    end