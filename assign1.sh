#!/bin/sh

echo "QUESTION 1 RUNNING..."
chmod 777 neighbor-districts-generator.sh
./neighbor-districts-generator.sh
echo "QUESTION 1 RUN SUCCESSFUL"

echo "QUESTION 2 RUNNING..."
chmod 777 edge-generator.sh
./edge-generator.sh
echo "QUESTION 2 RUN SUCCESSFUL"

echo "QUESTION 3 RUNNING..."
chmod 777 case-generator.sh
./case-generator.sh
echo "QUESTION 3 RUN SUCCESSFUL"

echo "QUESTION 4 RUNNING..."
chmod 777 peaks-generator.sh
./peaks-generator.sh
echo "QUESTION 4 RUN SUCCESSFUL"

echo "QUESTION 5 RUNNING..."
chmod 777 vaccinated-count-generator.sh
./vaccinated-count-generator.sh
echo "QUESTION 5 RUN SUCCESSFUL"

echo "QUESTION 6 RUNNING..."
chmod 777 vaccination-population-ratio-generator.sh
./vaccination-population-ratio-generator.sh
echo "QUESTION 6 RUN SUCCESSFUL"

echo "QUESTION 7 RUNNING..."
chmod 777 vaccine-type-ratio-generator.sh
./vaccine-type-ratio-generator.sh
echo "QUESTION 7 RUN SUCCESSFUL"

echo "QUESTION 8 RUNNING..."
chmod 777 vaccinated-ratio-generator.sh
./vaccinated-ratio-generator.sh
echo "QUESTION 8 RUN SUCCESSFUL"

echo "QUESTION 9 RUNNING..."
chmod 777 complete-vaccination-generator.sh
./complete-vaccination-generator.sh
echo "QUESTION 9 RUN SUCCESSFUL"

echo " "
echo "output files(.csv) have been saved in 'output files' folder !"

