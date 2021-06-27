# SOFOSKOGustav
Repository containing the work for SOFOSKO of summer 2021.



Conditions set up to define if a mutation is within a specific annotated region:
#1 START of mutation is BEFORE the annotated START and end of mutation is AFTER the annotated START
#2 START of mutation is BEFORE annotated END and end of mutation is AFTER annotated END
#3 -||- and end of mutation is UNDEFINED (numpy.NaN)