%% INTRODUCTION
% TITLE: Parsing and Analysis script for csv data
% PROJECT: STL inferencing of black-box data
% DATE: 14 JAN 24
% AUTHORS: J. Mockler
% DESC: This script parses and plots RL-controlled mario kart agents. As
% well, it makes higher order approximations of derived quantities

clear; close all
addpath("parsed_agent_data")

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

x_pos = smoothdata(x_pos);
y_pos = smoothdata(y_pos, 'movmean', 3);

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

phi = body_angle(x_pos, y_pos).*180/pi;
phi_dot = first_derivative(phi, ts);

figure (2)
set(gca,'TickLabelInterpreter','latex')

subplot(4,2,1); hold on;
plot(ts, x_pos); grid minor; 
ylabel('\textbf{x pos, m}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,3); hold on;
plot(ts, x_velocity); grid minor; 
ylabel('\boldmath $v_x$, \textbf{m/s}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,5); hold on;
plot(ts, x_acc); grid minor; 
ylabel('\boldmath $a_x$, \textbf{m/s$^2$}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,7)
plot(ts, phi); grid minor; 
ylabel('\boldmath $\psi$, \textbf{deg}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])
xlabel('\textbf{Time steps}', 'Interpreter','latex')

subplot(4,2,2); hold on;
plot(ts, y_pos); grid minor; 
ylabel('\textbf{y pos, m}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,4); hold on;
plot(ts, y_velocity); grid minor; 
ylabel('\boldmath $v_y$, \textbf{m/s}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,6); hold on;
plot(ts, y_acc); grid minor; 
ylabel('\boldmath $a_y$, \textbf{m/s$^2$}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

subplot(4,2,8)
plot(ts, phi_dot); grid minor; 
ylabel('\boldmath $\dot{\psi}$, \textbf{deg/s}', 'interpreter','latex', 'FontSize',10); xlim([0, 40])

xlabel('\textbf{Time steps}', 'Interpreter','latex')

sgtitle('\textbf{Derived State Data}', 'interpreter', 'latex', 'FontSize',13)


% Fig 3 - Plot the trajectory
figure (3)
plot(x_pos, y_pos, '-*')
grid minor
ylabel('\textbf{y position}', 'interpreter', 'latex'); 
xlabel('\textbf{x position}', 'interpreter', 'latex')
title('\textbf{Agent Trajectory}', 'interpreter', 'latex', 'FontSize',13)
set(gca,'TickLabelInterpreter','latex')

% Add some arrows to indicate trajectory
% do every 'arrow_plot_step' steps
arrow_plot_step = 5; j = 1;
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

% Now overlay the track
startx = -110; starty = -20;
dim = 4200;
image_data = imread('Racetrack_map.jpg');
img_obj = image(image_data, 'xdata', [startx, startx+ dim], 'ydata', ...
   [starty, starty+ dim], 'AlphaData', 0.20);


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

end % end agent loop

fprintf('\nPlotting complete.')
fprintf('\n--------------------------------\n')
