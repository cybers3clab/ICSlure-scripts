% Code to initialize parameters for sscv_wind_turbine

% Copyright 2021-22 The MathWorks, Inc.

load('sscv_wind_turbine_Cp.mat')                         % Loading wind turbine power coefficient table
load('sscv_wind_turbine_MPPT.mat')                       % Loading MPPT characteristics - omega vs wind speed
                                                         % and active power demand vs wind speed
load('sscv_wind_turbine_Derating.mat')                   % Loading derating table - wind speed vs pitch angle


% Rotor hub and gear train parameters
turbineRadius               = 70.5/2;                    % (m) Turbine radius
rotorBladeInertia           = 3963845;                   % (kg*m^2) Low speed side inertia
generatorInertia            = 200;                       % (kg*m^2) High speed side inertia
carrierShaftInertia         = 10;                        % (kg*m^2) Carrier Shaft inertia
stepShaftInertia            = 10;                        % (kg*m^2) Step Shaft inertia
ringSunTeethRatio           = 5;                         % (1) Ring to sun teeth ratio
firstStepTeethRatio         = 3.05;                      % (1) Follower to base teeth ratio
secondStepTeethRatio        = 3.05;                      % (1) Follower to base teeth ratio
airDensity                  = 1.15;                      % (kg/m^3) Air density
vWindThreshold              = 0.01;                      % (m/s) Threshold wind velocity to avoid divison by zero in Tip Speed Ratio calculation
wThreshold                  = 0.01;                      % (rad/s) Threshold wind turbine velocity for numerical convergence
gearRatio                   = 55.815;                    % (1) Gear train gear ratio
cpBraking                   = -0.001;                    % (1) Power coefficient for aerodynamic braking
inizialStressThreshold      = 500e3;                     % (W) Inzitial stress threshold for nominal operation
wearRate                    = 0.033;                     % (1) Rate of reduction of stress threshold for year of operation
stressRateRelease           = 0.05;                      % (1) Rate of reduction of stress for second of nominal operation
cumulativeStressThreshold   = 1.5e6;                     % (W*s) Threshold for cumulative stress fault
initialOperationTime        = 0;                         % (s) Second of operation at simulation start

% Turbine state machine parameters
vWindCutInLower             = 4;                         % (m/s) Cut in lower wind speed
vWindCutOut                 = 20;                        % (m/s) Cut out wind speed
vWindCutInUpper             = 0.9*vWindCutOut;           % (m/s) Cut in upper wind speed
vWindRated                  = 12;                        % (m/s) Rated wind speed
wTurbineCutIn               = 11;                        % (rpm) Turbine cut in speed
wTurbineCutOut              = 22;                        % (rpm) Turbine cut out speed
wTurbinePark                = 0.2*wTurbineCutIn;         % (rpm) Turbine parking speed


% Pitch controller parameters
pitchBrakeAngle             = 95;                        % (deg) Emergency pitch brake angle
minPitchAngle               = min(pitch);                % (deg) Minimum pitch angle
maxPitchAngle               = max(pitch);                % (deg) Maximum pitch angle
actuatorRampRate            = 20;                        % (deg/s) Pitch actuator angle change ramp rate
controllerTimeConstant      = 2;                         % (s) Controller time constant
turbineRatedPower           = 1.5;                       % (MW) Wind turbine rated power
pGenerationGain             = 0.1;                       % Proportional gain for power derating
iGenerationGain             = 1;                         % Integral gain for power derating

% Extending power coefficient table in aerodynamic pitch brake region
numTSR                      = size(cp,2);                % Estimating size of power coefficient table
pitch                       = [pitch,90,95];             % (deg) Extending pitch angle vector to brake region
cp                          = [cp;cpBraking*ones(2,numTSR)]; % Power coefficient table extension to braking region

% Park brake parameters
brakePressure               = 100;                       % (bar) Park brake pressure
brakeTorqueRadius           = 0.7;                       % (m) Brake pack radius
numFrictionSurfaces         = 5;                         % (1) Number of brake pack frction surface
brakePistonArea             = 0.65;                      % (m^2) Brake piston area
brakeStaticFrictionCoeff    = 0.8;                       % (1) Brake static friction coefficient
brakeKineticFrictionCoeff   = 0.7;                       % (1) Brake kinetic friction coefficient
brakeClutchVelocityTol      = 1e-3;                      % (rad/s) Brake clutch velocity tolerance
brakeThresholdPressure      = 100;                       % (Pa) Engagement threshold pressure

% Simplified Generator, Grid, and Transformer parameters
transformerRatedPower       = 1.8;                       % (MW) Transformer rated power
generatorEfficiency         = 90;                        % (1) Generator efficiency
wAtGeneratorRatedPower      = wTurbineCutOut*gearRatio;  % (rpm) Generator speed for derating control
wGeneratorBrakeLimit        = 0.50;                      % (1) Generator reference speed ratio for pitch brake control
pGeneratorBrakeLimit        = 0.50;                      % (1) Generator reference power ratio for pitch brake control


% Wind profile selection and simulation time

% Setting up variant subsystem
windProfile1=Simulink.Variant('windProfile==1');
windProfile2=Simulink.Variant('windProfile==2');
windProfile3=Simulink.Variant('windProfile==3');

windProfile                 = 1;                         % Selection of wind profile
if windProfile==1
    simT                    = 80;                        % (sec) Simulation time
elseif windProfile==2
    simT                    = 270;                       % (sec) Simulation time
else
    simT                    = 100;                       % (sec) Simulation time
end