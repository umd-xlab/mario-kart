# State Variables

## Independent Variables
Independent variables can be classified as environment or controlled variables; these variables are related to factors over which the system does not have control. The values of the environment variables may change arbitrarily over an execution.
### Controlled
These variables have values that are directly determined by the control protocol.
1. Power supplied to flight controllers that control the altitude
2. Vehicular state ('land', 'hover', 'move to landing zone 2', return to base', or 'mission complete'). Detailed in [[#LTL Specifications for Vehicle State]]
### Environment
1. Wind speed (approximated with a four-level quantization *wind speed = {low, medium, high, hurricane}*)
2. Terrain incline
3. People in the landing zone (boolean variable that is either 0 or 1, and will eventually drop to 0)
## Dependent Variables
These variables are dependent on the controlled and environmental variables.
- Altitude
- Vehicular Orientation - specifically pitch, but more generally, pose
- Vehicle longitude/latitude
	- This may be within the set of coordinates pre-defined by the mission.
# Requirements of the System
## Safety Requirements
*These capture the conditions that must be maintained in order for the system to operate safely.*
1. Power cannot be below minimum capacity nor above maximum capacity.
2.  The vehicle cannot move to the 'land' state if it has poor altitude stability.
	1. Altitude stability is dependent on the power supplied (controlled variable)
	2. Altitude stability is also dependent on the wind speed (environment variable)
	3. See Assumptions 1. 
3.  The vehicle cannot move to the 'land' state if people are in the current landing zone.
	1. If there exists people in the landing zone, the vehicle must continue to hover.
4. The vehicle must move to Landing Zone 2 if there are objects in Landing Zone 1.
	1. We assume objects are immovable.
5. The vehicle can only land within a specific defined area called a landing zone, defined by a polygonal box drawn on the map
	1. Two landing zones exist; titled Landing Zone 1 and Landing Zone 2.
	2. The vehicle must compare its current position (lat/long) with the landing zone it is currently targeting.
## Performance Requirements
*These specify the desired operating conditions of the system.*
1. The terrain does not exceed 5% inclination
## Assumptions
*These assumptions on the behavior of the environment are included to restrict the environment behavior into its admissible range & make sure that the desired properties are achievable.* 
1. If the windspeed is less than hurricane for 5 continuous time steps AND within the power supply, the altitude stability is good.

# Vehicular State Specifications

Linked from [[#Controlled]]. 
The valid vehicle states are:
1. 'return to base'
2. 'hover'
3. 'move to landing zone 2'
4. 'land' 

![[Landing Problem Setup 2024-03-06 15.56.53.excalidraw|800]]

# Altitude Stability Specifications
![[LTL to Behavior Trees Research 2024-02-26 13.08.59.excalidraw|800]]

# Vehicular Information (Pose, Location) Specifications
![[Landing Problem Setup 2024-03-07 09.59.43.excalidraw|800]]
