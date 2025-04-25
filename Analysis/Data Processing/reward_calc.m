%% INTRODUCTION
% TITLE: Reward Calculation
% DESC: This script calculates the reward to get an approximate idea of the
% cumulative reward across the series

% ACCEPTS: x_pos == array: x positions to calculate over. 
%          y_pos == array: y position to calculate over
%          checkpoints == array: current checkpoint list
%          surface == array: surfaces traveled on by the agent
%          speed == array: array of the speed (L2 of the velocity)
% RETURNS: rwd_series == array: reward time history
%          cum_rwd == float: cumulative reward

function [rwd_series, cum_rwd] = reward_calc(x_pos, y_pos, checkpoints, surface, speed, time_sec)

N = length(x_pos);

speed_rwd = zeros(1,N);
% Do the speed reward
for i = 1:N
    if speed(i) > 500
        speed_rwd(i) = 5;
    elseif speed(i) > 0
        speed_rwd(i) = 1;
    else
        speed_rwd(i) = -25;
    end

    % Check if backward - very simply checks if the agent moves backward
    % from the starting line
    if y_pos(i) > (y_pos(1) + 10)
        speed_rwd(i) = -20;
    end

end

check_rwd = zeros(1,N);
% Do the checkpoint reward
% First turn all 29 checkpoints into -1's so we can loop correctly
for i = 1:length(checkpoints)
    if checkpoints(i) == 29
        checkpoints(i) = -1;
    end
end

for i = 2:N
    if checkpoints(i) > checkpoints(i-1)
        check_rwd(i) = 50;
    elseif checkpoints(i) < checkpoints(i-1)
        check_rwd(i) = -100;
    else
        check_rwd(i) = 0;
    end
end

% Do time reward
time_end = time_sec(N);
time_reward = zeros(1,N);

if time_end < 6
    time_reward(end) = 500;
elseif time_end < 7
    time_reward(end)  = 400;
elseif time_end < 8
    time_reward(end)  = 300;
elseif time_end < 9
    time_reward(end)  = 200;
elseif time_end < 10
    time_reward(end)  = 100;
else
    time_reward(end)  = 0;
end

% Finally do the road reward
road_rwd = zeros(1, N);
for i = 1:N
    if surface(i) ~= 64
        road_rwd(i) = -3;
    elseif surface(i) == 64
        road_rwd(i) = 4;
    end
end

rwd_series = road_rwd + check_rwd + speed_rwd + time_reward;
cum_rwd = sum(rwd_series);

figure
sgtitle('Reward Components')
subplot(2,2,1);
plot(1:N, road_rwd); ylabel('Road Reward')
grid on; 

subplot(2,2,2)
plot(1:N, check_rwd); ylabel('Checkpoint Reward')
grid on; 

subplot(2,2,3)
plot(1:N, speed_rwd); ylabel('Speed Reward')
xlabel('Time index'); grid on;

subplot(2,2,4)
plot(1:N, time_reward); ylabel('Time Reward')
xlabel('Time index'); grid on;

end
