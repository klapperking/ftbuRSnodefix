@ECHO OFF

:: Path to java.exe (JRE 8 default) ::
set javapath=C:\Program Files\Java\jre1.8.0_251\bin\java.exe

:: Allocated memory ::
set mem=8G

:: Server jar ::
set jar=forge-1.16.5-36.2.26.jar

echo.
ECHO Java Version: %javapath%
echo.
ECHO Starting the server...
echo.

"%javapath%" -Xmx%mem% -Xms%mem% -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true -jar %jar% nogui
pause