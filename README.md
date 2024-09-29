This is full script of FLAC3D for undergroupd train station under seismic loading

1. Sequence of Running FLAC3D
[1_N]GenModel.f3dat
[2_N]ConTunnel.f3dat
[3_N]GenShell.f3dat
[4_N]DynamicPrep_3Motions.f3dat
-> You can change input motions at this script
[5_N]DynamicRun_3Motions.f3dat

Then it will create .sav files for Max. Acc., Vel., Disp., time of the input motion
After getting the each save files,

You can create output graphs using Python script using
[P_N]PostProsess.py
[P_N]PostProsessForce.py

It is recommended to execute the above Python script in FLAC3D. Otherwise, installation of Python module is reuqired for each environment.

"tunnel.f3grid" is finite difference element grid for FLAC3D made by Griddle and Rhino,

Enjoy!



