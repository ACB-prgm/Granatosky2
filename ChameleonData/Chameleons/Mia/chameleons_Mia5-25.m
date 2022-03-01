% nicholas flaim
% CAML
% determining duty factor and stride time/length

close all
clear
clc
%% MUST BE CHANGED WHEN IMPLEMENTED INTO ORIGINAL CODE
conversion = 0.000135316; %%calculate this by taking known snout-vent measurement (in meters) divided by the snout-vent pixel distance

%% fps of camera
fps = 120;                          % frames per second
%% enters ExtractedData
currentfolder = pwd;
% cd ExtractedData;
% cd DigitizedFile;
%% user selects file and back out to original folder
filename = uigetfile('.csv');       % user selects file
%% data is extracted from digitized file and return to ExtractedData folder
data = readmatrix(filename);     % reads numerical values from .csv file
dataraw = readtable(filename);
cd ..;
%% changing first column to seconds
data(:,1) = data(:,1)/fps;
%% sign convention due to DLC being a pain in the ___
if data(1,12) > data(size(data,1),12)
    sign = -1;
else
    sign = 1;
end

%% plotting
figure(1)
subplot(2,1,1)
plot(data(:,1),data(:,20));      % plotting eyeX vs time
title('ankleX vs. Time [s]');
subplot(2,1,2)
plot(data(:,1),data(:,11));     % plotting wingY vs time
title('wristX vs. Time [s]');
grid on
%% ginput
tbound = mean(data(:,1));       % initialize
times = NaN(100,1);
counter = 1;
while tbound > min(data(:,1)) && tbound < max(data(:,1))
            [tbound,~] = ginput(1);
            times(counter) = tbound;
            counter = counter + 1;
end
times = times(~isnan(times));
if rem(length(times),2) == 1
    error('You mucked up the selection process, please ensure an odd number of points are picked before selecting outside the data');
end
times(size(times,1)) = [];
times = sort(times);

a= times(1,1);
b= times(2,1);
c= times(3,1);

a1 = round2actual(data(:,1),a); 
b1 = round2actual(data(:,1),b); 
c1 = round2actual(data(:,1),c); 

[wrist,~] = ginput(1);
time2 = wrist;

%% velocity calculation 

velstart = find(a1 == data(:,1));
velstop = find(c1 == data(:,1)); 

veldata = data(velstart:velstop,:);

last = length(veldata); 

%% putting into matrix
abc = NaN(floor(length(times)/2),8);
% columns are [a,b,c,stride time,stance phase,swing phase,duty factor,stride length [m]]

abc(1,1:3) = [a,b,c];
abc(1,4) = c-a;
abc(1,5) = b-a;
abc(1,6) = c-b; 
abc(1,7) = (b-a) / (c-a);
abc(1,8) = (veldata(length(veldata),20) - veldata(1,20))*conversion ;


dia = (time2 - abc(1,1))/(abc(1,3)-abc(1,1));
velocity = abc(1,8)/abc(1,4); 
%% table
tab =[abc(:,1),abc(:,2),abc(:,3),abc(:,4),abc(:,5),abc(:,6),abc(:,7),abc(:,8),dia, velocity];
    
datalabels = {'a' 'b' 'c' 'stride time [s]' 'stance phase [s]' 'swing phase [s]'...
    'duty factor []' 'stride length [m]', 'diagonality', 'velocity'};

tab = mat2cell(tab,ones(1,size(tab,1)),ones(1,size(tab,2)));
finaloutput =[datalabels ; tab]; 

% finaltable(1,:) = datalabels;
% finaltable(2,:) = tab;

tabavg = table(mean(abc(:,7)),mean(abc(:,8)),'VariableNames',...
    {'Avg Duty Factor' 'Avg Stride Length [m]'});
%% functions
function [coordAct] = round2actual(data, coordGinput)

[mdata, ndata] = size(data);
[minput,ninput] = size(coordGinput);
lengGinput = length(coordGinput);
diff = zeros(mdata, ndata);
coordAct = zeros(minput,ninput);

for j = 1:lengGinput
    for n = 1:ndata
        for m = 1:mdata
            diff(m,n) = abs(data(m,n) - coordGinput(j));
        end
    end
    minimum = min(diff);
    location = find(minimum == diff);
    if length(location) > 1
        location = location(1);
    end
    coordAct(j) = data(location,1);
end
coordAct = sort(coordAct);              % sorts values in ascending order
end