# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:13:32 2019

@author: dsampietro
"""

import Fab_processing_functions_4_centroide as fb
import numpy as np
import time
import os

start_time =time.time()
first_start_time =time.time()
cwd = os.getcwd()
Log = open('log.txt','w')
#Inputs
#Numb of files to explit to avoid memory errors
numb_files_to_explit = 8
#####################INPUTS############################################################################
Realizations=['07']#INTRODUCIR EL NOMBRE DE LAS REALIZACIONES A ANALIZAR. SI HAY MAS DE UNA HAY QUE MODIFICAR A PARTIR DE LINEA 34 PARA HACER UN  FOR

##Coordinates to filtrate
xmax= 6729
xmin= 5599
ymax= 9425
ymin= 8254
zmax= -20
zmin=-426.7817
#Input to Filter by transmisivity
threshold=[1e-8,1e-7,1e-6]#valor de transmisividad para seleccionar
prop_position=1 #position of the property in the fab (NO TOCAR SI PROVIENE DE DARCYTOOLS)
########################################################################################################
i=0 #Esto es por el loop 
#Empezar loop cuando toque
Master_folder=["/Realization"+Realizations[i]]  #Añadir mas carpetas si se quiere correr en varios
input_path=str(cwd+Master_folder[0]+"/Fractures_ECPM/fractures/")

try:
    for r in range(0,len(threshold)):
        path=input_path+'results/Fab_filtered_by_coordinates/T'+str(threshold[r])+'/'
        os.makedirs(path)
        print('Directory '+input_path+'results/Fab_filtered_by_coordinates/T'+str(threshold[r])+'/'+' created')
        Log.write('Directory '+input_path+'results/Fab_filtered_by_coordinates/T'+str(threshold[r])+'/'+' created'+'\n')
except:
  print("Results directory exists")
  Log.write("Results directory exists"+'\n')
results_path = input_path+'/results/'

Input_file=input_path+'r'+Realizations[i]+'_c1.fab'
Coordinates_file=results_path+'r'+Realizations[i]+'coordinates.dat'
Coordinates_file_center=results_path+'r'+Realizations[i]+'coordinates_with_center.dat'
fab_filtered_coordinates_location=input_path+'results/Fab_filtered_by_coordinates/'
file_explit_name='r'+Realizations[i]+'coordinates_with_center.dat'


###Obtaining coordinates
print("Obtaining coordinates")
Log.write("Obtaining coordinates"+'\n')
fb.fabreader_obtaining_coordinates(Input_file,Coordinates_file)
print("finished (Obtaining coordinates)")
Log.write("finished (Obtaining coordinates)"+'\n')
print("Computing center polygon")
Log.write("Computing center polygon"+'\n')
fb.compute_center_polygon(Coordinates_file,Coordinates_file_center)
print("finished (Computing center polygon)")
Log.write("finished (Computing center polygon)"+'\n')
Log.write("Expliting files"+'\n')
print("Expliting files")
fb.file_explit(file_explit_name,numb_files_to_explit,results_path)
print("finished (Expliting files)")
Log.write("finished (Expliting files)"+'\n')

print("Filtering fractures ID")
Log.write("Filtering fractures ID"+'\n')
Coordinates_file_filtered='r'+Realizations[i]+'coordinates_filtered.dat'
for j in range(1,numb_files_to_explit+1):
    print("filtering file "+ str(j)+ " of "+str(numb_files_to_explit))
    Log.write("filtering file "+ str(j)+ " of "+str(numb_files_to_explit)+'\n')
    fb.filtered_fractures_con_centro(results_path+str(j)+'_'+file_explit_name,results_path+str(j)+'_'+Coordinates_file_filtered,xmax,xmin,ymax,ymin,zmax,zmin)
    print("Finished filtering file "+str(j)+" of "+str(numb_files_to_explit))
    Log.write("Finished filtering file "+str(j)+" of "+str(numb_files_to_explit)+'\n')
#Merge files
print("Merging filtered ID files")
Log.write("Merging filtered ID files"+'\n')
fb.merge_files(Coordinates_file_filtered,numb_files_to_explit,results_path)
Input_file_matrix= 'merged_file.txt'
print("finished (Merging filtered ID files)")
Log.write("finished (Merging filtered ID files)"+'\n')
print("Generating filtered files")
Log.write("Generating filtered files"+'\n')
# Generate filtered file by coordinates
Fab_filtered_coordinates_name = 'r'+Realizations[i]+'filtered_by_coordiantes.fab'
fb.fabreader_filtering_coordinates(Input_file,fab_filtered_coordinates_location+Fab_filtered_coordinates_name,results_path+Input_file_matrix)
print("finished (Generating filtered files)")
Log.write("finished (Generating filtered files)"+'\n')
#Extracting_properties
print("Extracting_properties")
Log.write("Extracting_properties"+'\n')

#Fab_filtered_coordinates_name = 'r'+Realizations[i]+'filtered_by_coordiantes.fab'
Threshold_folder_path=input_path+'results/Fab_filtered_by_coordinates/'
matrix_file=Threshold_folder_path+'Properties.txt'
fb.extract_properties_file(fab_filtered_coordinates_location+Fab_filtered_coordinates_name,matrix_file)
print("finished (Extracting_properties)")
Log.write("finished (Extracting_properties)"+'\n')
OutputName = 'r'+Realizations[i]+'.fab'
print("Filtering files")
Log.write("Filtering files"+'\n')
for i in range(0,len(threshold)):
    Threshold_folder_path_T=input_path+'results/Fab_filtered_by_coordinates/T'+str(threshold[i])+'/'
    fb.fabreader_filtering_coordinates_by_properties(fab_filtered_coordinates_location+Fab_filtered_coordinates_name,OutputName,matrix_file, threshold[i], prop_position, Threshold_folder_path_T)
End_time =time.time()
Simulation_time= End_time- first_start_time
print("Finished (Filtering files)")
Log.write("Finished (Filtering files)"+'\n')
print("Total execution time of "+ str(Simulation_time)+ " seconds or "+ str(Simulation_time/60)+ " Minutes")
Log.write("Total execution time of "+ str(Simulation_time)+ " seconds or "+ str(Simulation_time/60)+ " Minutes"+'\n')
Log.close()
