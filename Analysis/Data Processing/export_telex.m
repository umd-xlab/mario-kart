%% INTRODUCTION
% TITLE: Orientation angle calculation
% DESC: This script numerically calculates the body's orientation w.r.t
% its starting value (assuming reference is forward at start)

% ACCEPTS: states == arrays: arrays of states to save off - must update
%          function if you want additional to save off
%          names == array of strings: names as col headers for the data
% RETURNS: state_space.csv: a csv file in ___ folder that can be used
%          directly with TeLEx

function export_telex(time, phi_dot, v, names)
% First check if arrays are in cols
if length(time(1,:)) ~= 1
    time = time';
end
if length(phi_dot(1,:)) ~= 1
    phi_dot = phi_dot';
end
if length(v(1,:)) ~= 1
    v = v';
end

% Now put into a table
T = array2table([time, phi_dot, v],...
    "VariableNames", names);

% Save off data as a csv
writetable(T,".\TeLEx_DATA\TeLExData.csv")

fprintf('\nData successfully exported to TeLEx_DATA subfolder!')

end