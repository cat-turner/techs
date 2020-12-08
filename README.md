# Techs
An api that tells you the distance between technicians. 

This api accespts two query parameters:
* unit: the unit of the calculated distance betweem the two technicians. Accepted units are "m" (meters) and ft (feet).
* name: the name of the technician

default: If no values are provided, the distances between all technicians will be shown in meters. The response includes a flag that tells you if the technicians are within 1000ft of one another.
