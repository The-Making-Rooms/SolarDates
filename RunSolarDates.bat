@echo off
color 60
echo Uzair wuz here.


:prog
cls
cd C:\Users\TMR_Staff\Desktop\EphemerisData\
C:\Users\TMR_Staff\AppData\Local\Programs\Python\Python311\python.exe "C:\Users\TMR_Staff\Desktop\EphemerisData\solar_Dates_NFM22.py"
echo Program errored out. Press enter to attempt restart.
pause 

goto prog