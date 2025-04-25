%% INTRODUCTION
% TITLE: Parsing and Analysis script for csv data
% PROJECT: STL inferencing of black-box data
% DATE: 14 JAN 24
% AUTHORS: J. Mockler
% DESC: This script parses and plots RL-controlled mario kart agents. As
% well, it makes higher order approximations of derived quantities

clear; close all
addpath("parsed_agent_data")
overlay_tracker=0;

for agent = 1 % loop and plot the 8 agents
% agents are grouped by their data, so just pull out the correct name
agent_data_name = ['mario_kart_data_agent', num2str(agent), '.csv'];

%% Parsing

fprintf('--------------------------------')
fprintf('\nAnalyzing agent number %i', agent)
fprintf('\n--------------------------------')
fprintf('\nBegin parsing!')
agent_traj = readtable(agent_data_name);
agent_traj = agent_traj{:,:};

ts = agent_traj(:,1);
x_pos = agent_traj(:,2);
y_pos = agent_traj(:,3);
checkpoints = agent_traj(:,4);
surfaces = agent_traj(:,5);
ingame_speed = agent_traj(:,6);

% This is the approx time of gameplay - as of 31MAR25, we don't save it
% off, so I'm hard-coding it. Note: it's around 15 time steps == 1 sec,
% but it does vary slightly due to frame skip
time_sec = [0*ones(1,50), 1*ones(1,15), 2*ones(1,15), 3*ones(1,15), ...
    4*ones(1,15), 5*ones(1,15), 6*ones(1,15), 7*ones(1,15), 8*ones(1,15),...
    9*ones(1,15), 10*ones(1,15), 11*ones(1,15), 12*ones(1,15), ...
    13*ones(1, 15), 14*ones(1,15), 15*ones(1,15)];

% Now detect when a 'reset' has occured, where the agent moves back to the
% starting line. The following line chops the data to right before the
% reset time step
[flag, idx, x_pos, y_pos] = reset_detection(x_pos, y_pos);
ts = ts(1:idx);
if flag == 1
    fprintf('\nA reset has occured at time step %i', idx)
    fprintf('\nTime series data will be chopped!')
elseif flag == 0
    fprintf('\nNo reset has occured! Data will remain in full length')
end

x_pos(1) = 3711; x_pos(2) = 3711; x_pos(3) = 3711; x_pos(4) = 3711;
x_pos(5) = 3711;

x_start = x_pos(1); x_end = x_pos(end);
y_start = y_pos(1); y_end = y_pos(end);
fprintf('\nParsing complete.')

% Lightly smooth the data to counter map discretization
x_pos = smoothdata(x_pos, 'movmean', 3);
y_pos = smoothdata(y_pos, 'movmean', 3);

% Take additional data off?
data_pts_off = 0;
x_pos = x_pos(1:end-data_pts_off);
y_pos = y_pos(1:end-data_pts_off);
ts = ts(1:end-data_pts_off);


%% Plotting
fprintf('\nBegin plotting!')
% Fig 1 - plot the raw data as subplots
figure (1)
sgtitle('Raw agent data')

subplot(2,1,1); hold on
plot(ts, x_pos)
ylabel('x position')
grid minor

subplot(2,1,2); hold on
plot(ts, y_pos)
ylabel('y position'); xlabel('time steps')
grid minor

% Fig 2 - plot some derived quantities
x_velocity = first_derivative(x_pos, ts);
y_velocity = first_derivative(y_pos, ts);

x_acc = first_derivative(x_velocity, ts);
y_acc = first_derivative(y_velocity, ts);

%x_acc = second_derivative(x_pos, ts);
%y_acc = second_derivative(y_pos, ts);

phi = body_angle(x_pos, y_pos, x_velocity, y_velocity).*180/pi;
phi_dot = first_derivative(phi, ts);

figure (2)
set(gca,'TickLabelInterpreter','latex')

subplot(4,2,1); hold on;
plot(ts, x_pos); grid minor; 
ylabel('\textbf{x pos, m}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

subplot(4,2,3); hold on;
plot(ts, x_velocity); grid minor; 
ylabel('\boldmath $v_x$, \textbf{m/s}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

subplot(4,2,5); hold on;
plot(ts, x_acc); grid minor; 
ylabel('\boldmath $a_x$, \textbf{m/s$^2$}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

subplot(4,2,7)
plot(ts, phi); grid minor; 
ylabel('\boldmath $\psi$, \textbf{deg}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])
xlabel('\textbf{Time steps}', 'Interpreter','latex')

subplot(4,2,2); hold on;
plot(ts, y_pos); grid minor; 
ylabel('\textbf{y pos, m}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

subplot(4,2,4); hold on;
plot(ts, y_velocity); grid minor; 
ylabel('\boldmath $v_y$, \textbf{m/s}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

subplot(4,2,6); hold on;
plot(ts, y_acc); grid minor; 
ylabel('\boldmath $a_y$, \textbf{m/s$^2$}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])
subplot(4,2,8)
plot(ts, phi_dot); grid minor; 
ylabel('\boldmath $\dot{\psi}$, \textbf{deg/s}', 'interpreter','latex', 'FontSize',10); xlim([0, length(x_pos)])

xlabel('\textbf{Time steps}', 'Interpreter','latex')

sgtitle('\textbf{Derived State Data}', 'interpreter', 'latex', 'FontSize',13)


% Fig 3 - Plot the trajectory
figure (3); hold on
plot(x_pos, y_pos, '-*')
grid minor
ylabel('\textbf{y position}', 'interpreter', 'latex'); 
xlabel('\textbf{x position}', 'interpreter', 'latex')
title('\textbf{Agent Trajectory}', 'interpreter', 'latex', 'FontSize',13)
set(gca,'TickLabelInterpreter','latex')

% Add some arrows to indicate trajectory
% do every 'arrow_plot_step' steps
arrow_plot_step = 9; j = 1;
x_arrow_list = []; y_arrow_list = []; u_arrow_list = []; v_arrow_list = [];
for i = 1:length(x_pos)
    if mod(i, arrow_plot_step) == 0
        x_arrow_list(j) = x_pos(i);
        y_arrow_list(j) = y_pos(i);
        u_arrow_list(j) = mean(x_velocity(i-2:i+2))/5;
        v_arrow_list(j) = mean(y_velocity(i-2:i+2))/5;
        j = j+1;
    end
end
hold on

quiver(x_arrow_list, y_arrow_list, u_arrow_list, v_arrow_list,...
    0.5,'LineWidth',2)
axis equal

% plot s.t it resembles the mario kart track orientation better
set(gca, 'YDir','reverse') 
legend('Agent trajectory', 'Direction of travel', 'interpreter','latex')

if overlay_tracker == 0
    % Now overlay the track
    startx = -110; starty = -20;
    dim = 4200;
    image_data = imread('Racetrack_map.jpg');
    img_obj = image(image_data, 'xdata', [startx, startx+ dim], 'ydata', ...
       [starty, starty+ dim], 'AlphaData', 0.20);
    overlay_tracker = 1;
end


% Fig 4 - plot the speed and acceleration magnitude
speed = (x_velocity.^2 + y_velocity.^2).^(1/2);
acc_mag = (x_acc.^2 + y_acc.^2).^(1/2);

figure (4)
subplot(2,1,1); hold on
plot(ts, speed); grid minor; ylabel('speed')
subplot(2,1,2); hold on
plot(ts, acc_mag); grid minor; ylabel('accel magnitude')
xlabel('Time steps')
sgtitle('Speed and Acceleration Magnitudes')

%% Calculate the cumulative reward
[rwd_series, cum_rwd] = reward_calc(x_pos, y_pos, checkpoints, surfaces, ingame_speed, time_sec);
fprintf('Cumulative reward: %4.2f', cum_rwd)

% Fig 5 - plotting the rwd series
figure
plot(ts, rwd_series); grid minor; 
ylabel('R(i)'); xlabel('Time steps')
title(['Reward Profile: Integrated Total = ', num2str(cum_rwd)])

end % end agent loop

%% TeLEx Export Data
% Header names - must be a vector of strings!
header_names=["time","phidot","speed"];
%export_telex(ts, phi_dot, speed, header_names)


%% Statement plotting
% This section will plot the 3 pSTL statements on the graph
% statement 1: when above phidot > 0.5, what's the speed upper limit?
% figure
% subplot(2,1,1); hold on;
% plot(ts, phi_dot)
% %yline(-0.5, 'r--')
% grid minor; ylabel('\boldmath $\dot{\psi}$, \textbf{deg/s}', 'interpreter','latex', 'FontSize',10);
% 
% subplot(2,1,2); hold on;
% plot(ts, speed)
% yline(39.61, 'r--')
% grid minor; xlabel('\textbf{Time steps}', 'Interpreter','latex'); ylabel('\textbf{$V$, m/s}', 'Interpreter','latex')
% sgtitle('\textbf{Overlaid pSTL-Mined Properties}', 'interpreter', 'latex', 'FontSize',13)
% 
% % statement 2: When does the speed first reach 20 m/s?
% subplot(2,1,1);
% 
% subplot(2,1,2);
% xline(32.004, 'k-.')
% 
% % statement 3: how long is the agent engaged in a turn?
% subplot(2,1,1); hold on;
% xline(41.003, ':', 'color', 	"#7E2F8E", 'LineWidth',1.5)
% xline(54.994, ':', 'color', 	"#7E2F8E", 'LineWidth',1.5)
% xlim([0,72]); ylim([-12,1])
% 
% subplot(2,1,2); hold on;
% xline(41.003, ':', 'color', 	"#7E2F8E", 'LineWidth',1.5)
% xline(54.994, ':', 'color', 	"#7E2F8E", 'LineWidth',1.5)
% xlim([0,72])

fprintf('\nPlotting complete.')
fprintf('\n--------------------------------\n')
