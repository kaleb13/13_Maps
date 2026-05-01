@echo off
echo =======================================================
echo RouteOpt - OSRM Local Setup Script
echo =======================================================
echo.
echo Make sure Docker Desktop is running before continuing!
pause

echo.
echo Step 1/3: Extracting map data...
docker run -t -v "%cd%\osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/ethiopia-latest.osm.pbf

echo.
echo Step 2/3: Partitioning map data...
docker run -t -v "%cd%\osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/ethiopia-latest.osrm

echo.
echo Step 3/3: Customizing map data...
docker run -t -v "%cd%\osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/ethiopia-latest.osrm

echo.
echo =======================================================
echo Pre-processing complete!
echo Starting OSRM Server on http://localhost:5000...
echo Keep this window open. Press Ctrl+C to stop.
echo =======================================================
docker run -t -i -p 5000:5000 -v "%cd%\osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/ethiopia-latest.osrm
