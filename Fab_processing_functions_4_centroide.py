# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:49:47 2019

@author: dsampietro
"""

import matplotlib.pyplot as plt
import fileinput
import numpy as np
import os
import time
import gc
def fabreader_obtaining_coordinates(fileName,OutputName):
    print("working: Reading the fab file "+ fileName)
    #cwd = os.getcwd()
    #input_path=cwd+'/fab/'
    #results_path = cwd+'/results/'

    # Open file

    f = open(fileName, 'r')
    vertex_file = open(OutputName,'w')
#INITIALIZE
    Properties_name=[]
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Numb_fractures=0
    Numb_properties=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    line_numb = 0
    counter=0
    for line in f:
        line = line.strip()
        columns = line.split()
        line_numb = line_numb+1
        if len(columns)>0:
            #print("PRUEBA")
            if columns[0]=='BEGIN'or columns[0]=='Begin':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                    Format_Section = 1
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 1
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =1
                else:
                    kk=0
        ###########################################
            elif columns[0]=='END' or columns[0]=='End':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                   Format_Section = 0
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 0
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =0
                else:
                    kk=0
            else:
                kk=0
        ###########################################
            if Format_Section == 1:
                if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                    Numb_fractures= columns[2]
                elif columns[0]=='No_properties'or columns[0]=='NumProperties':
                    Numb_properties= columns[2]
                else:
                    kk=0
            else:
                kk=0
        ###########################################
            if Properties_Section == 1:
                if columns[0]=="BEGIN":
                    kk=0
                else:
                    Properties_name.append(columns[3])
            else:
                    mm=0
            if Fracture_Section == 1:
                if columns[0]=="BEGIN":
                    init = -10
                    fracture_index_counter=0
                else:                      
                    if init ==-10:
                        index_frac=columns[0]
                        #index_frac=counter
                        if int(index_frac)==0:
                            fracture_index_counter=fracture_index_counter+1
                            numb_vertex = int(columns[1])
                            vertex_file.write(str(fracture_index_counter)+"\t")
                            init = fracture_index_counter
                        else:
                            numb_vertex = int(columns[1])
                            #vertex_file.write(str(index_frac)+"\t")
                            vertex_file.write(str(columns[0])+"\t")#Asi se mantiene el ID del Fab para luego buscarlo
                            init = int(index_frac)**2

                    else:
                        if columns[0]== str(0):
                            qq= "COORDINATES SECTION"
                            #print(str(columns[1]))
                            if int(counter)<=int(Numb_fractures):
                                init=-10
                                vertex_file.write("\n")
                                counter+=1
                                if float(counter)%100000==0:
                                    print( str(float(counter)/float(Numb_fractures)*100)+"% readed" )
                                else:
                                    a=0
                            else:
                                kk=0
                        else:
                            vertex_file.write(str(columns[1])+"\t"+str(columns[2])+"\t"+str(columns[3])+"\t")
            else:
                kk=0
        else:
            y=0
    f.close()
    vertex_file.close()
    print("Finished")
def compute_center_polygon(fileName,OutputName): #Esto es valido siempre que tenga 4 cordenadas
    #cwd = os.getcwd()
    #input_path=cwd+'/results/'
    #results_path = cwd+'/results/'
    f = open(fileName, 'r')
    numlines=0
    Mediax=[]
    Mediay=[]
    Mediaz=[]
    for line in f:
        line = line.strip()
        columns = line.split()
        numlines+=1
        if float(numlines)%100000==0:
            print("Fractura "+ str(numlines))
        else:
            a=0
        Mediax.append((float(columns[1])+float(columns[4])+float(columns[7])+float(columns[10]))/4)
        Mediay.append((float(columns[2])+float(columns[5])+float(columns[8])+float(columns[11]))/4)
        Mediaz.append((float(columns[3])+float(columns[6])+float(columns[9])+float(columns[12]))/4)
    f.close()
    q = open(fileName, 'r')
    f = open(OutputName, 'w')
    numlines=0
    for line in q:
        line = line.strip()        
        f.write(line+"\t"+str(Mediax[numlines])+"\t"+str(Mediay[numlines])+"\t"+str(Mediaz[numlines])+"\n")
        numlines+=1
    f.close()
    q.close()
def filtered_fractures_con_centro(fileName,OutputName, xmax,xmin,ymax,ymin,zmax,zmin):
    #cwd = os.getcwd()
    #input_path=cwd+'/results/'
    #results_path = cwd+'/results/'
    AOriginal = np.genfromtxt(fileName,skip_header=0)
    mat = np.array(AOriginal)
    numcols = np.size(mat,1)
    numb_vertex=(numcols-4)/3
    if numb_vertex== 3:
        print("number of vertex is 3")
        print("No considera el centro")
        mat2= mat[(mat[:,1]>xmin)&(mat[:,1]<xmax)|(mat[:,4]>xmin)&(mat[:,4]<xmax)|(mat[:,7]>xmin)&(mat[:,7]<xmax)|(mat[:,2]>ymin)&(mat[:,2]<ymax)|(mat[:,5]>ymin)&(mat[:,5]<ymax)|(mat[:,8]>ymin)&(mat[:,8]<ymax)|(mat[:,3]>zmin)&(mat[:,3]<zmax)|(mat[:,6]>zmin)&(mat[:,6]<zmax)|(mat[:,9]>zmin)&(mat[:,9]<zmax)]

    elif numb_vertex==4:
        print("number of vertex is 4")
        #mat2= mat[(mat[:,1]>xmin)&(mat[:,1]<xmax)|(mat[:,4]>xmin)&(mat[:,4]<xmax)|(mat[:,7]>xmin)&(mat[:,7]<xmax)|(mat[:,10]>xmin)&(mat[:,10]<xmax) |(mat[:,2]>ymin)&(mat[:,2]<ymax)|(mat[:,5]>ymin)&(mat[:,5]<ymax)|(mat[:,8]>ymin)&(mat[:,8]<ymax)|(mat[:,11]>ymin)&(mat[:,11]<ymax)|(mat[:,3]>zmin)&(mat[:,3]<zmax)|(mat[:,6]>zmin)&(mat[:,6]<zmax)|(mat[:,9]>zmin)&(mat[:,9]<zmax)|(mat[:,12]>zmin)&(mat[:,12]<zmax)]
        mat2= mat[(mat[:,1]>xmin)&(mat[:,1]<xmax)|(mat[:,4]>xmin)&(mat[:,4]<xmax)|(mat[:,7]>xmin)&(mat[:,7]<xmax)|(mat[:,10]>xmin)&(mat[:,10]<xmax)|(mat[:,13]>xmin)&(mat[:,13]<xmax)]
        mat3= mat2[(mat2[:,2]>ymin)&(mat2[:,2]<ymax)|(mat2[:,5]>ymin)&(mat2[:,5]<ymax)|(mat2[:,8]>ymin)&(mat2[:,8]<ymax)|(mat2[:,11]>ymin)&(mat2[:,11]<ymax)|(mat2[:,14]>ymin)&(mat2[:,14]<ymax)]
        mat4= mat3[(mat3[:,3]>zmin)&(mat3[:,3]<zmax)|(mat3[:,6]>zmin)&(mat3[:,6]<zmax)|(mat3[:,9]>zmin)&(mat3[:,9]<zmax)|(mat3[:,12]>zmin)&(mat3[:,12]<zmax)|(mat3[:,15]>zmin)&(mat3[:,15]<zmax)]
    else:
        print("Number of vertex of the fractures not considered in the script, improve it...Line 134")
    ID_filtered = (mat4[:,0])
    ID_filtered=ID_filtered.astype(int)
    np.savetxt(OutputName,ID_filtered, fmt='%d')
    
    '''
def filtered_fractures(fileName,OutputName, xmax,xmin,ymax,ymin,zmax,zmin):#obsoleta
    cwd = os.getcwd()
    input_path=cwd+'/results/'
    results_path = cwd+'/results/'
    AOriginal = np.genfromtxt(input_path+fileName,skip_header=0)
    mat = np.array(AOriginal)
    numcols = np.size(mat,1)
    numb_vertex=(numcols-1)/3
    if numb_vertex== 3:
        print("number of vertex is 3")
        mat2= mat[(mat[:,1]>xmin)&(mat[:,1]<xmax)|(mat[:,4]>xmin)&(mat[:,4]<xmax)|(mat[:,7]>xmin)&(mat[:,7]<xmax)|(mat[:,2]>ymin)&(mat[:,2]<ymax)|(mat[:,5]>ymin)&(mat[:,5]<ymax)|(mat[:,8]>ymin)&(mat[:,8]<ymax)|(mat[:,3]>zmin)&(mat[:,3]<zmax)|(mat[:,6]>zmin)&(mat[:,6]<zmax)|(mat[:,9]>zmin)&(mat[:,9]<zmax)]

    elif numb_vertex==4:
        print("number of vertex is 4")
        mat2= mat[(mat[:,1]>xmin)&(mat[:,1]<xmax)|(mat[:,4]>xmin)&(mat[:,4]<xmax)|(mat[:,7]>xmin)&(mat[:,7]<xmax)|(mat[:,10]>xmin)&(mat[:,10]<xmax) |(mat[:,2]>ymin)&(mat[:,2]<ymax)|(mat[:,5]>ymin)&(mat[:,5]<ymax)|(mat[:,8]>ymin)&(mat[:,8]<ymax)|(mat[:,11]>ymin)&(mat[:,11]<ymax)|(mat[:,3]>zmin)&(mat[:,3]<zmax)|(mat[:,6]>zmin)&(mat[:,6]<zmax)|(mat[:,9]>zmin)&(mat[:,9]<zmax)|(mat[:,12]>zmin)&(mat[:,12]<zmax)]
    else:
        print("Number of vertex of the fractures not considered in the script, improve it...Line 134")
    ID_filtered = (mat2[:,0])
    ID_filtered=ID_filtered.astype(int)
    np.savetxt(results_path+OutputName,ID_filtered, fmt='%d')
    '''
    
    

def fabreader_filtering_coordinates(fileName,OutputName,matrix_file):
    print("working: Filtering the fab file "+ fileName)
    #cwd = os.getcwd()
    #input_path=cwd+'/fab/'
    #matrix_path=cwd+'/results/'
    #results_path = cwd+'/fab_results/'
    # Open file
    #f = open(input_path+fileName, 'r')
    print("Generating new fab files")
    wselected = open(OutputName,'w')
    wdiscarted = open(OutputName+'Discarted','w')
    print("Opening matrix with index to be selected")
    q = open(matrix_file,'r')
    Index_matrix=[]
    linenumb=0
    for line in q:
        line = line.strip()
        columns = line.split()
        Index_matrix.append(int(columns[0]))
        if float(linenumb)%500000==0:
            print("Leyendo linea "+str(linenumb))
            linenumb+=1
        else:
            linenumb+=1
    matrix = Index_matrix
    print("Matrix readed")

    Properties_name=[]

    Numb_fractures=0
    Numb_properties=0
    Num_selected=0
    Num_non_selected=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    fracture_index_counter=0
    current_line=0
    Numb_fractures_to_select= len(matrix)
    #matrix=matrix.tolist()
    print("The filtering is in execution")
    #for line in f:
    contador_lineas = 0
    with open(fileName) as file:
        for line in file:
            contador_lineas += 1
           #print( "linea "+str(contador_lineas))
            line = line.strip()
            columns = line.split()
            if len(columns)>0:
                #print("PRUEBA")
                if columns[0]=='BEGIN':
                    if columns[1] == 'FORMAT' or columns[1]=='Format':
                        Format_Section = 1
                        wselected.write('BEGIN FORMAT'+'\n')
                        wdiscarted.write('BEGIN FORMAT'+'\n')
                    elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                        Properties_Section = 1
                        wselected.write('BEGIN PROPERTIES'+'\n')
                        wselected.write('Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                        wselected.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                        wselected.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                        wdiscarted.write('BEGIN PROPERTIES'+'\n')
                        wdiscarted.write(' Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                        wdiscarted.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                        wdiscarted.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                    elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                        Fracture_Section =1
                        wselected.write(' BEGIN FRACTURE'+'\n')
                        wdiscarted.write(' BEGIN FRACTURE'+'\n')
                    elif columns[1]=='SETS' or columns[1]=='Sets':
                        wselected.write(' BEGIN SETS'+'\n')
                        wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                        wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                        wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                        wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                        wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                        wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                        wdiscarted.write(' BEGIN SETS'+'\n')
                        wdiscarted.write('Set1    =    "SetDefinition_1"'+'\n')
                        wdiscarted.write('Set2    =    "SetDefinition_2"'+'\n')
                        wdiscarted.write('Set3    =    "SetDefinition_3"'+'\n')
                        wdiscarted.write('Set4    =    "SetDefinition_4"'+'\n')
                        wdiscarted.write('Set5    =    "SetDefinition_5"'+'\n')
                        wdiscarted.write('Set6    =    "SetDefinition_6"'+'\n')
                    else:
                        kk=0
                    #wselected.write(line+'\n')
                    #wdiscarted.write(line+'\n')
                        
            ###########################################
                elif columns[0]=='END' or columns[0]=='End':
                    if columns[1] == 'FORMAT' or columns[1]=='Format':
                        wselected.write('END FORMAT'+'\n')
                        wdiscarted.write('END FORMAT'+'\n')
                        Format_Section = 0
                    elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                        Properties_Section = 0
                        wselected.write('END PROPERTIES'+'\n')
                        wdiscarted.write('END PROPERTIES'+'\n')
                        '''
                        wselected.write('BEGIN SETS'+'\n')
                        wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                        wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                        wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                        wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                        wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                        wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                        wselected.write('END SETS'+'\n')
                        wdiscarted.write('BEGIN SETS'+'\n')
                        wdiscarted.write('Set1    =    "SetDefinition_1"'+'\n')
                        wdiscarted.write('Set2    =    "SetDefinition_2"'+'\n')
                        wdiscarted.write('Set3    =    "SetDefinition_3"'+'\n')
                        wdiscarted.write('Set4    =    "SetDefinition_4"'+'\n')
                        wdiscarted.write('Set5    =    "SetDefinition_5"'+'\n')
                        wdiscarted.write('Set6    =    "SetDefinition_6"'+'\n')
                        wdiscarted.write('END SETS'+'\n')
                        '''
                    elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                        Fracture_Section =0
                        wselected.write('END FRACTURE'+'\n')
                        wdiscarted.write('END FRACTURE'+'\n')
                    else:
                        kk=0
                    #wselected.write(line+'\n')
                    #wdiscarted.write(line+'\n')
                else:
                    kk=0
            ###########################################
                if Format_Section == 1:
                    if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                        Numb_fractures= columns[2]
                        wselected.write('No_Fractures = '+str(len(matrix))+'\n')
                        wdiscarted.write('No_Fractures = '+str(int(Numb_fractures)-len(matrix))+'\n')
                    elif columns[0]=='No_properties' or columns[0]=='NumProperties':
                        Numb_properties= columns[2]
                        wselected.write('No_properties = 3'+'\n')
                        wdiscarted.write('No_properties = 3'+'\n')
                        wselected.write('No_sets = 6'+'\n')
                        wdiscarted.write('No_sets = 6'+'\n')
                    elif columns[0] == 'Begin' or columns[0] == 'BEGIN':
                        kkkk=0
                    else:
                        kk=0
                        wselected.write(line+'\n')
                        wdiscarted.write(line+'\n')
                else:
                    kk=0
            ###########################################
                if Properties_Section == 1:
                    if columns[0]=="BEGIN":
                        kk=0
                    else:
                        Properties_name.append(columns[3])
                        #wselected.write(line+'\n')
                        #wdiscarted.write(line+'\n')
                else:
                        mm=0
                if Fracture_Section == 1:
                    if columns[0]=="BEGIN":
                        first_start_time =time.time()
                        qq=0
                        init = -99999999999999
                        Bolean=-100
                    else:                  
                        if init ==-99999999999999:
                            index_frac= columns[0]
                            
                            if int(index_frac) == 0:
                                fracture_index_counter = fracture_index_counter+1
                                index_frac = fracture_index_counter
                            else:
                                qwe=0
                             
                            numb_vertex = int(columns[1])
                            init = int(index_frac)
                            #nx= np.any(np.equal(float(index_frac), matrix))
                            if len(matrix)==0:
                                matrix.append(-99999)
                            else:
                                df=0
                            Numb_fractures_readed= Num_selected+ Num_non_selected
                            if float(index_frac)==float(matrix[0]):
                                if int(index_frac)<=0:
                                    wselected.write(str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean = 100
                                    Num_selected= Num_selected+1
                                else:
                                    wselected.write('-'+str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean = 100
                                    Num_selected= Num_selected+1
                                matrix.pop(0)
                                if float(Num_selected)%50000==0:
                                    print( "-----------------"+str(float(Num_selected)/float(Numb_fractures_to_select)*100)+"% founded -------------------" )
                                else:
                                    a=0
                            else:
                                if int(index_frac)<=0:
                                    #wdiscarted.write(str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean =-100
                                    Num_non_selected=Num_non_selected+1
                                else:
                                    #wdiscarted.write('-'+str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean =-100
                                    Num_non_selected=Num_non_selected+1
                            if float(Numb_fractures_readed)%500000==0:
                                print(str(float(Numb_fractures_readed)/float(Numb_fractures)*100)+" % readed")
                            else:
                                a=0
                            if float(Numb_fractures_readed)%50000==0:
                                print( str(Numb_fractures_readed)+" fractures readed"+' of '+ str(Numb_fractures) )
                            else:
                                a=0
                                '''
                            if float(Numb_fractures_readed)>=700000:
                                print( str(Numb_fractures_readed)+" fractures readed"+' of '+ str(Numb_fractures) )
                                print( "-----------------Fractures selected "+str(float(Num_selected)))
                            else:
                                a=0
                                '''
                        else:
                            if columns[0]== str(0):
                                qq= "COORDINATES SECTION"
                                #print(str(columns[1]))
                                #init=-99999999999999
                                if int(Numb_fractures_readed)<=int(Numb_fractures):
                                    init=-99999999999999
                                else:
                                    kk=0
                                current_line=current_line+1
    #                            if current_line%100000==0:
    #                                print("current fracture is "+ str(current_line)+' of '+ str(Numb_fractures))
                                #endtime =time.time()
                                #print("time is "+str(first_start_time-endtime))
                                #print("time is "+str(first_start_time-endtime))
    #                            else:
    #                                asd=0
                            else:
                                qq=0
                            if Bolean ==100:
                                wselected.write(line+'\n')
                            else:
                                q=0
                                #wdiscarted.write(line+'\n')
                else:
                    kk=0
               #gc.collect()
            else:
                y=0
        wselected.write('BEGIN TESSFRACTURE'+'\n')
        wselected.write('END TESSFRACTURE'+'\n')    
        wselected.write('BEGIN ROCKBLOCK'+'\n')
        wselected.write('END ROCKBLOCK'+'\n')   
        wdiscarted.write('BEGIN TESSFRACTURE'+'\n')
        wdiscarted.write('END TESSFRACTURE'+'\n')    
        wdiscarted.write('BEGIN ROCKBLOCK'+'\n')
        wdiscarted.write('END ROCKBLOCK'+'\n')   
        print("ENDING "+fileName)
        print("SELECTED "+str(Num_selected)+" fractures")
        print("NON SELECTED "+str(Num_non_selected)+" fractures")
        #f.close()
        wselected.close()
        wdiscarted.close()
        #print(PropStore)





def cubic_law(aperture,density,gravity,viscosity):
    Trans = gravity*density/(12*viscosity)*(float(aperture)**3)
    return Trans




def extract_properties_file_to_aperture(fileName,OutputName):
    print("working: Reading the fab file "+ fileName)
    cwd = os.getcwd()
    input_path=cwd+'/fab_results/'
    results_path = cwd+'/fab_results/'

    
    
    ##############################♣
    f = open(input_path+fileName, 'r')

    x=0
    Fortmat_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Properties_name=[]
    kkkkk=0
    x=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Apertures =[]
    
    Numb_fractures=0
    Numb_properties=0
    
    
    
    def properties():
            if columns[0]=="BEGIN":
                kk=0
            else:
                Properties_name.append(columns[3])
            return Properties_name
        
    def Fracture_processor():
        
        return
        
        
    kkkkk=0
    x=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Apertures =[]
    for line in f:
        line = line.strip()
        columns = line.split()
       # print(columns)
    
    
        if len(columns)>0:
            #print("PRUEBA")
            if columns[0]=='BEGIN':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                    Format_Section = 1
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 1
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =1
                else:
                    kk=0
                    
                    
        ###########################################
            elif columns[0]=='END' or columns[0]=='End':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                   Format_Section = 0
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 0
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =0
                else:
                    kk=0
            else:
                kk=0
        ###########################################
            if Format_Section == 1:
                if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                    Numb_fractures= columns[2]
                elif columns[0]=='No_properties'or columns[0]=='NumProperties':
                    Numb_properties= columns[2]
                else:
                    kk=0
                
            else:
                kk=0
        ###########################################
            if Properties_Section == 1:
                if columns[0]=="BEGIN":
                    kk=0
                else:
                    Properties_name.append(columns[3])
                PropStore = np.zeros((int(Numb_fractures),1+int(len(Properties_name))))
            else:
                    mm=0
            if Fracture_Section == 1:
                if columns[0]=="BEGIN":
                    qq=0
                    kkkkk=10000
                    init = -10
                else:                  
                    if init ==-10:
                        index_frac=columns[0]
                        numb_vertex = int(columns[1])
                        PropStore[int(index_frac)-1,0]=index_frac
                        for i in range(0,int(Numb_properties)):
                            PropStore[int(index_frac)-1,i+1]=columns[3+i]
                        init = int(columns[0])
                        #print('Fracture '+str(index_frac)+' of '+ str(Numb_fractures))
                    else:
                        if columns[0]== str(0):
                            qq= "COORDINATES SECTION"
                            #print(str(columns[1]))
                            if int(index_frac)<=int(Numb_fractures):
                                init=-10
                            else:
                                kk=0
                        else:
                            qq=0
    
                #Fracture_processor()
            else:
                kk=0
    
        else:
            y=0
    #print("Number of fractures is "+str(Numb_fractures))
    
    lst = map(str, Properties_name)  
    line = " ".join(lst)
    np.savetxt(results_path+OutputName, PropStore,header= '"ID fracture" '+(line) ,fmt='%1.10e')
    
    
    
    
    #print("END")
    f.close()
    #print(PropStore)



def matrix_ordered_to_aperture(Filename,column, threshold):
    print('Working in getting the Fracture ID')
    cwd = os.getcwd()
    input_path=cwd+'/fab_results/'
    column = int(column)
    threshold = int(threshold)
    matrix =np.genfromtxt(input_path+Filename,skip_header=1)

    #a = matrix[matrix[:,column].argsort(kind='mergesort')]
    a = matrix[matrix[:,column].argsort()]
    # matrix_Reorder= matrix[np.lexsort(matrix.T[column])]
    #print(a)
    numb_frac = np.size(a,0)
    New_matrix = np.zeros(threshold)
    for i in range(0,threshold):
        New_matrix[i]=int(a[numb_frac-threshold+i,0])
    print('Finish to order the matrix')
    return New_matrix



def fabreader_filter_aperture(fileName,OutputName,matrix,threshold):
    print("working: Filtering the fab file "+ fileName)
    cwd = os.getcwd()
    input_path=cwd+'/fab_results/'
    results_path = cwd+'/final_fab/'
    # Open file
    f = open(input_path+fileName, 'r')
    wselected = open(results_path+'Selected_'+str(threshold)+'_'+OutputName,'w')
    wtoECPM = open(results_path+'To_ecpm_'+str(threshold)+'_'+OutputName,'w')
    #print(f.read())
    
    density = 1000
    gravity = 9.81
    viscosity = 0.001

    Fortmat_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Properties_name=[]
    kkkkk=0
    x=0
    Apertures =[]
    
    Numb_fractures=0
    Numb_properties=0
    Num_selected=0
    Num_non_selected=0
    
    def properties():
            if columns[0]=="BEGIN":
                kk=0
            else:
                Properties_name.append(columns[3])
            return Properties_name

    kkkkk=0
    x=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Apertures =[]
    for line in f:
        line = line.strip()
        columns = line.split()

        if len(columns)>0:
            #print("PRUEBA")
            if columns[0]=='BEGIN':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                    Format_Section = 1
                    wselected.write('BEGIN FORMAT'+'\n')
                    wtoECPM.write('BEGIN FORMAT'+'\n')
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 1
                    wselected.write('BEGIN PROPERTIES'+'\n')
                    wselected.write('Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                    wselected.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                    wselected.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                    wtoECPM.write('BEGIN PROPERTIES'+'\n')
                    wtoECPM.write(' Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                    wtoECPM.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                    wtoECPM.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =1
                    wselected.write(' BEGIN FRACTURE'+'\n')
                    wtoECPM.write(' BEGIN FRACTURE'+'\n')
                elif columns[1]=='SETS' or columns[1]=='Sets':
                    wselected.write(' BEGIN SETS'+'\n')
                    wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                    wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                    wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                    wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                    wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                    wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                    wtoECPM.write(' BEGIN SETS'+'\n')
                    wtoECPM.write('Set1    =    "SetDefinition_1"'+'\n')
                    wtoECPM.write('Set2    =    "SetDefinition_2"'+'\n')
                    wtoECPM.write('Set3    =    "SetDefinition_3"'+'\n')
                    wtoECPM.write('Set4    =    "SetDefinition_4"'+'\n')
                    wtoECPM.write('Set5    =    "SetDefinition_5"'+'\n')
                    wtoECPM.write('Set6    =    "SetDefinition_6"'+'\n')
                else:
                    kk=0
                #wselected.write(line+'\n')
                #wtoECPM.write(line+'\n')
                    
        ###########################################
            elif columns[0]=='END' or columns[0]=='End':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                    wselected.write('END FORMAT'+'\n')
                    wtoECPM.write('END FORMAT'+'\n')
                    Format_Section = 0
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 0
                    wselected.write('END PROPERTIES'+'\n')
                    wtoECPM.write('END PROPERTIES'+'\n')
                    wselected.write('BEGIN SETS'+'\n')
                    wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                    wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                    wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                    wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                    wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                    wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                    wselected.write('END SETS'+'\n')
                    wtoECPM.write('BEGIN SETS'+'\n')
                    wtoECPM.write('Set1    =    "SetDefinition_1"'+'\n')
                    wtoECPM.write('Set2    =    "SetDefinition_2"'+'\n')
                    wtoECPM.write('Set3    =    "SetDefinition_3"'+'\n')
                    wtoECPM.write('Set4    =    "SetDefinition_4"'+'\n')
                    wtoECPM.write('Set5    =    "SetDefinition_5"'+'\n')
                    wtoECPM.write('Set6    =    "SetDefinition_6"'+'\n')
                    wtoECPM.write('END SETS'+'\n')
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =0
                    wselected.write('END FRACTURE'+'\n')
                    wtoECPM.write('END FRACTURE'+'\n')
                else:
                    kk=0
                #wselected.write(line+'\n')
                #wtoECPM.write(line+'\n')
            else:
                kk=0
        ###########################################
            if Format_Section == 1:
                if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                    Numb_fractures= columns[2]
                    wselected.write('No_Fractures = '+str(threshold)+'\n')
                    wtoECPM.write('No_Fractures = '+str(int(Numb_fractures)-int(threshold))+'\n')
                elif columns[0]=='No_properties' or columns[0]=='NumProperties':
                    Numb_properties= columns[2]
                    wselected.write('No_properties = 3'+'\n')
                    wtoECPM.write('No_properties = 3'+'\n')
                    wselected.write('No_sets = 6'+'\n')
                    wtoECPM.write('No_sets = 6'+'\n')
                elif columns[0] == 'Begin' or columns[0] == 'BEGIN':
                    kkkk=0
                else:
                    kk=0
                    wselected.write(line+'\n')
                    wtoECPM.write(line+'\n')
            else:
                kk=0
        ###########################################
            if Properties_Section == 1:
                if columns[0]=="BEGIN":
                    kk=0
                else:
                    Properties_name.append(columns[3])
                    #wselected.write(line+'\n')
                    #wtoECPM.write(line+'\n')
                PropStore = np.zeros((int(Numb_fractures),1+int(len(Properties_name))))

            else:
                    mm=0
            if Fracture_Section == 1:
                if columns[0]=="BEGIN":
                    qq=0
                    kkkkk=10000
                    init = -10
                    Bolean=-100
                else:                  
                    if init ==-10:
                        index_frac=columns[0]
                        numb_vertex = int(columns[1])
                        PropStore[int(index_frac)-1,0]=index_frac
                        for i in range(0,int(Numb_properties)):
                            PropStore[int(index_frac)-1,i+1]=columns[3+i]
                        init = int(columns[0])
          #              print('Fracture '+str(index_frac)+' of '+ str(Numb_fractures))
                        if float(index_frac) in matrix:
                            wselected.write('-'+str(columns[0])+' '+ str(columns[1])+' '+str(columns[2])+' '+str(cubic_law(columns[3],density,gravity, viscosity))+'  11  '+str(columns[3])+'\n')
                            Bolean = 100
                            Num_selected= Num_selected+1
                        else:
                            Bolean = -100
                            wtoECPM.write('-'+str(columns[0])+' '+ str(columns[1])+' '+str(columns[2])+' '+str(cubic_law(columns[3],density,gravity, viscosity))+'  11  '+str(columns[3])+'\n')
                            Num_non_selected=Num_non_selected+1
                    else:
                        if columns[0]== str(0):
                            qq= "COORDINATES SECTION"
                            #print(str(columns[1]))
                            if int(index_frac)<=int(Numb_fractures):
                                init=-10
                            else:
                                kk=0
                        else:
                            qq=0
                        if Bolean ==100:
                            wselected.write(line+'\n')
                        else:
                            wtoECPM.write(line+'\n')
            else:
                kk=0
        else:
            y=0
    wselected.write('BEGIN TESSFRACTURE'+'\n')
    wselected.write('END TESSFRACTURE'+'\n')    
    wselected.write('BEGIN ROCKBLOCK'+'\n')
    wselected.write('END ROCKBLOCK'+'\n')   
    wtoECPM.write('BEGIN TESSFRACTURE'+'\n')
    wtoECPM.write('END TESSFRACTURE'+'\n')    
    wtoECPM.write('BEGIN ROCKBLOCK'+'\n')
    wtoECPM.write('END ROCKBLOCK'+'\n')   
    print("ENDING "+fileName)
    print("SELECTED "+str(Num_selected)+" fractures")
    print("NON SELECTED "+str(Num_non_selected)+" fractures")
    f.close()
    wselected.close()
    wtoECPM.close()
    #print(PropStore)


def file_explit(input_file,number_of_files,results_path):
    #cwd = os.getcwd()
    #input_path=cwd+'/results/'
    results_path = results_path
    f=open(results_path+input_file,'r')
    num_lines = 0
    for line in f:
        num_lines =num_lines+1
    #num_lines= 107220218
    breakpoint=int(num_lines/number_of_files)
    
    f.close()
    f=open(results_path+input_file,'r')
    if int(number_of_files) == 2:
        g=open(results_path+'1_'+input_file,'w')
        h=open(results_path+'2_'+input_file,'w')
        line_counter=0
        for line in f:
            line = line.strip()
            if int(line_counter) <int(breakpoint):
                g.write(line)
                g.write("\n")
            else:
                g.close()
                h.write(line)
                h.write("\n")
            line_counter = line_counter+1
            if line_counter%10000==0:
                print( str(line_counter)+ " of "+ str(num_lines))
        #g.close()
        f.close()
        h.close()
    elif int(number_of_files)==4:
        g=open(results_path+'1_'+input_file,'w')
        h=open(results_path+'2_'+input_file,'w')
        i=open(results_path+'3_'+input_file,'w')
        j=open(results_path+'4_'+input_file,'w')
        line_counter=0
        for line in f:
            line = line.strip()
            if int(line_counter) < int(breakpoint):
                g.write(line)
                g.write("\n")
            elif int(line_counter) <= int(2*breakpoint):
                g.close()
                h.write(line)
                h.write("\n")
            elif int(line_counter) <= int(3*breakpoint):
                h.close()
                i.write(line)
                i.write("\n")
            else:
                i.close()
                j.write(line)
                j.write("\n")
            line_counter= line_counter+1
            if line_counter%10000==0:
                print( str(line_counter)+ " of "+ str(num_lines))
        j.close()
    elif int(number_of_files)==8:
        g=open(results_path+'1_'+input_file,'w')
        h=open(results_path+'2_'+input_file,'w')
        i=open(results_path+'3_'+input_file,'w')
        j=open(results_path+'4_'+input_file,'w')
        k=open(results_path+'5_'+input_file,'w')
        l=open(results_path+'6_'+input_file,'w')
        m=open(results_path+'7_'+input_file,'w')
        n=open(results_path+'8_'+input_file,'w')
        line_counter=0
        for line in f:
            line = line.strip()
            if int(line_counter) < int(breakpoint):
                g.write(line)
                g.write("\n")
            elif int(line_counter) <= int(2*breakpoint):
                g.close()
                h.write(line)
                h.write("\n")
            elif int(line_counter) <= int(3*breakpoint):
                h.close()
                i.write(line)
                i.write("\n")
            elif int(line_counter) <= int(4*breakpoint):
                i.close()
                j.write(line)
                j.write("\n")
            elif int(line_counter) <= int(5*breakpoint):
                j.close()
                k.write(line) 
                k.write("\n")
            elif int(line_counter) <= int(6*breakpoint):
                k.close()
                l.write(line)
                l.write("\n")
            elif int(line_counter) <= int(7*breakpoint):
                l.close()
                m.write(line)
                m.write("\n")
            else:
                m.close()
                n.write(line)
                n.write("\n")
            line_counter= line_counter+1
    else:
        print("wrong number of files to explit")
    print("File explited correctly")

def merge_files(input_name,number_files,results_path):
    #cwd = os.getcwd()
    #input_path=cwd+'/results/'
    results_path = results_path
    if number_files==2:
        h=open(results_path+'merged_file.txt','w')
        f=open(results_path+'1_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'2_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        h.close()
    elif number_files==4:
        h=open(results_path+'merged_file.txt','w')
        f=open(results_path+'1_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'2_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f=open(results_path+'3_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'4_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        h.clsoe()
    elif number_files==8:
        h=open(results_path+'merged_file.txt','w')
        f=open(results_path+'1_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'2_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f=open(results_path+'3_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'4_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'5_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)
            h.write("\n")
        f.close()
        f=open(results_path+'6_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)   
            h.write("\n")
        f.close()
        f=open(results_path+'7_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line)    
            h.write("\n")
        f.close()
        f=open(results_path+'8_'+input_name,'r')      
        for line in f:
            line = line.strip()
            h.write(line) 
            h.write("\n")
        h.close()
    else:
        print("wrong number of files")
    print("Finished merging")
    
def extract_properties_file(fileName,OutputName):
    print("working: Reading the fab file "+ fileName)
    #cwd = os.getcwd()
    #input_path=cwd+'/fab/'
    #results_path = cwd+'/fab_results/'

    
    
    ##############################♣
    f = open(fileName, 'r')
    x=0
    Fortmat_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Properties_name=[]
    kkkkk=0
    x=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Apertures =[]
    
    Numb_fractures=0
    Numb_properties=0
    
    
    
    def properties():
            if columns[0]=="BEGIN":
                kk=0
            else:
                Properties_name.append(columns[3])
            return Properties_name
        
    def Fracture_processor():
        
        return
        
        
    kkkkk=0
    x=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    Current_frac=0
    Apertures =[]
    for line in f:
        line = line.strip()
        columns = line.split()
       # print(columns)
        if len(columns)>0:
            #print("PRUEBA")
            if columns[0]=='BEGIN':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                    Format_Section = 1
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 1
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =1
                else:
                    kk=0
                    
                    
        ###########################################
            elif columns[0]=='END' or columns[0]=='End':
                if columns[1] == 'FORMAT' or columns[1]=='Format':
                   Format_Section = 0
                elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                    Properties_Section = 0
                elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                    Fracture_Section =0
                else:
                    kk=0
            else:
                kk=0
        ###########################################
            if Format_Section == 1:
                if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                    Numb_fractures= columns[2]
                elif columns[0]=='No_properties'or columns[0]=='NumProperties':
                    Numb_properties= columns[2]
                else:
                    kk=0
                
            else:
                kk=0
        ###########################################
            if Properties_Section == 1:
                if columns[0]=="BEGIN":
                    kk=0
                else:
                    Properties_name.append(columns[3])
                PropStore = np.zeros((int(Numb_fractures),1+int(len(Properties_name))))
            else:
                    mm=0
            if Fracture_Section == 1:
                if columns[0]=="BEGIN":
                    qq=0
                    kkkkk=10000
                    init = -99999999
                else:                  
                    if init ==-99999999:
                        index_frac=columns[0]
                        numb_vertex = int(columns[1])
                        PropStore[abs(int((Current_frac))),0]=index_frac
                        for i in range(0,int(Numb_properties)):
                            PropStore[abs(int(Current_frac)),i+1]=columns[3+i]
                        init = int(columns[0])
                        #print('Fracture '+str(index_frac)+' of '+ str(Numb_fractures))
                        Current_frac+=1
                    else:
                        if columns[0]== str(0):
                            qq= "COORDINATES SECTION"
                            #print(str(columns[1]))
                            if int(Current_frac)<=int(Numb_fractures):
                                init=-99999999
                            else:
                                kk=0
                        else:
                            qq=0
                #Fracture_processor()
            else:
                kk=0
        else:
            y=0
    #print("Number of fractures is "+str(Numb_fractures))
    lst = map(str, Properties_name)  
    line = " ".join(lst)
    np.savetxt(OutputName, PropStore,header= '"ID fracture" '+(line) ,fmt='%1.10e')

    #print("END")
    f.close()
    #print(PropStore)
    
    
def fabreader_filtering_coordinates_by_properties(fileName,OutputName,matrix_file, threshold, prop_position,results_path):
    print("working: Filtering the fab file "+ fileName)
    #cwd = os.getcwd()
    #input_path=cwd+'/fab/'
    #matrix_path=cwd+'/fab_results/'
    #results_path = cwd+'/final_fab/'
    # Open file
    #f = open(input_path+fileName, 'r')
    print("Generating new fab files")
    wselected = open(results_path+'T_lower_than_'+str(threshold)+'_'+OutputName,'w')
    wdiscarted = open(results_path+'T_larger_than_'+str(threshold)+'_'+OutputName,'w')
    print("Opening matrix with index to be selected")

    matrix = np.genfromtxt(matrix_file,skip_header=1)
    threshold=float(threshold)
    Number_lower_than_threshold = np.sum(matrix[:,prop_position] <= threshold) 
    Number_larger_than_threshold = np.sum(matrix[:,prop_position] > threshold) 
    #Index_matrix = np.genfromtxt(matrix_path+matrix_file,skip_header=0)
    print("Matrix readed")

    Properties_name=[]
    Numb_fractures=0
    Numb_properties=0
    Num_selected=0
    Num_non_selected=0
    Format_Section = 0
    Properties_Section = 0
    Fracture_Section = 0
    fracture_index_counter=0
    current_line=0
    Numb_fractures_to_select= len(matrix)
    #matrix=matrix.tolist()
    print("The filtering is in execution")
    #for line in f:
    contador_lineas = 0
    contador_fracturas = 0
    with open(fileName) as file:
        for line in file:
            contador_lineas += 1
           #print( "linea "+str(contador_lineas))
            line = line.strip()
            columns = line.split()
            if len(columns)>0:
                #print("PRUEBA")
                if columns[0]=='BEGIN':
                    if columns[1] == 'FORMAT' or columns[1]=='Format':
                        Format_Section = 1
                        wselected.write('BEGIN FORMAT'+'\n')
                        wdiscarted.write('BEGIN FORMAT'+'\n')
                    elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                        Properties_Section = 1
                        wselected.write('BEGIN PROPERTIES'+'\n')
                        wselected.write('Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                        wselected.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                        wselected.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                        wdiscarted.write('BEGIN PROPERTIES'+'\n')
                        wdiscarted.write(' Prop1    =    (Real*4)    "Transmissivity"'+'\n')
                        wdiscarted.write('Prop2    =    (Real*4)    "Storativity"'+'\n')
                        wdiscarted.write('Prop3    =    (Real*4)    "Aperture"'+'\n')
                    elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                        Fracture_Section =1
                        wselected.write(' BEGIN FRACTURE'+'\n')
                        wdiscarted.write(' BEGIN FRACTURE'+'\n')
                    elif columns[1]=='SETS' or columns[1]=='Sets':
                        wselected.write(' BEGIN SETS'+'\n')
                        wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                        wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                        wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                        wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                        wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                        wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                        wselected.write(' END SETS'+'\n')
                        wdiscarted.write(' BEGIN SETS'+'\n')
                        wdiscarted.write('Set1    =    "SetDefinition_1"'+'\n')
                        wdiscarted.write('Set2    =    "SetDefinition_2"'+'\n')
                        wdiscarted.write('Set3    =    "SetDefinition_3"'+'\n')
                        wdiscarted.write('Set4    =    "SetDefinition_4"'+'\n')
                        wdiscarted.write('Set5    =    "SetDefinition_5"'+'\n')
                        wdiscarted.write('Set6    =    "SetDefinition_6"'+'\n')
                        wdiscarted.write(' END SETS'+'\n')
                    else:
                        kk=0
                    #wselected.write(line+'\n')
                    #wdiscarted.write(line+'\n')
                        
            ###########################################
                elif columns[0]=='END' or columns[0]=='End':
                    if columns[1] == 'FORMAT' or columns[1]=='Format':
                        wselected.write('END FORMAT'+'\n')
                        wdiscarted.write('END FORMAT'+'\n')
                        Format_Section = 0
                    elif columns[1] == 'PROPERTIES' or columns[1]=='Properties':
                        Properties_Section = 0
                        wselected.write('END PROPERTIES'+'\n')
                        wdiscarted.write('END PROPERTIES'+'\n')
                        '''
                        wselected.write('BEGIN SETS'+'\n')
                        wselected.write('Set1    =    "SetDefinition_1"'+'\n')
                        wselected.write('Set2    =    "SetDefinition_2"'+'\n')
                        wselected.write('Set3    =    "SetDefinition_3"'+'\n')
                        wselected.write('Set4    =    "SetDefinition_4"'+'\n')
                        wselected.write('Set5    =    "SetDefinition_5"'+'\n')
                        wselected.write('Set6    =    "SetDefinition_6"'+'\n')
                        wselected.write('END SETS'+'\n')
                        wdiscarted.write('BEGIN SETS'+'\n')
                        wdiscarted.write('Set1    =    "SetDefinition_1"'+'\n')
                        wdiscarted.write('Set2    =    "SetDefinition_2"'+'\n')
                        wdiscarted.write('Set3    =    "SetDefinition_3"'+'\n')
                        wdiscarted.write('Set4    =    "SetDefinition_4"'+'\n')
                        wdiscarted.write('Set5    =    "SetDefinition_5"'+'\n')
                        wdiscarted.write('Set6    =    "SetDefinition_6"'+'\n')
                        wdiscarted.write('END SETS'+'\n')
                        '''
                    elif columns[1]=='FRACTURE' or columns[1]=='Fracture':
                        Fracture_Section =0
                        wselected.write('END FRACTURE'+'\n')
                        wdiscarted.write('END FRACTURE'+'\n')
                    else:
                        kk=0
                    #wselected.write(line+'\n')
                    #wdiscarted.write(line+'\n')
                else:
                    kk=0
            ###########################################
                if Format_Section == 1:
                    if columns[0]=='No_Fractures' or columns[0]=='NumFractures':
                        Numb_fractures= columns[2]
                        wselected.write('No_Fractures = '+str(Number_lower_than_threshold)+'\n')
                        wdiscarted.write('No_Fractures = '+str(Number_larger_than_threshold)+'\n')
                    elif columns[0]=='No_properties' or columns[0]=='NumProperties':
                        Numb_properties= columns[2]
                        wselected.write('No_properties = 3'+'\n')
                        wdiscarted.write('No_properties = 3'+'\n')
                        wselected.write('No_sets = 6'+'\n')
                        wdiscarted.write('No_sets = 6'+'\n')
                    elif columns[0] == 'Begin' or columns[0] == 'BEGIN':
                        kkkk=0
                    else:
                        kk=0
                        wselected.write(line+'\n')
                        wdiscarted.write(line+'\n')
                else:
                    kk=0
            ###########################################
                if Properties_Section == 1:
                    if columns[0]=="BEGIN":
                        kk=0
                    else:
                        Properties_name.append(columns[3])
                        #wselected.write(line+'\n')
                        #wdiscarted.write(line+'\n')
                else:
                        mm=0
                if Fracture_Section == 1:
                    if columns[0]=="BEGIN":
                        first_start_time =time.time()
                        qq=0
                        init = -99999999999999
                        Bolean=-100
                    else:                  
                        if init ==-99999999999999:
                            index_frac= columns[0]
                            if int(index_frac) == 0:
                                fracture_index_counter = fracture_index_counter+1
                                index_frac = fracture_index_counter
                            else:
                                qwe=0
                            numb_vertex = int(columns[1])
                            init = int(index_frac)
                            #nx= np.any(np.equal(float(index_frac), matrix))
                            if len(matrix)==0:
                                matrix.append(-99999)
                            else:
                                df=0
                            Numb_fractures_readed= Num_selected+ Num_non_selected
                            if threshold>float(matrix[contador_fracturas,prop_position]):
                                if int(index_frac)<=0:
                                    wselected.write(str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean = 100
                                    Num_selected= Num_selected+1
                                    contador_fracturas+=1
                                else:
                                    wselected.write('-'+str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean = 100
                                    Num_selected= Num_selected+1
                                    contador_fracturas+=1
                                if float(Num_selected)%50000==0:
                                    print( "-----------------"+str(float(Num_selected)/float(Numb_fractures_to_select)*100)+"% founded -------------------" )
                                else:
                                    a=0
                            else:
                                if int(index_frac)<=0:
                                    wdiscarted.write(str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean =-100
                                    Num_non_selected=Num_non_selected+1
                                    contador_fracturas+=1
                                else:
                                    wdiscarted.write('-'+str(index_frac)+' '+ str(columns[1])+' '+str(columns[2])+' '+str(columns[3])+' '+str(Num_selected)+' '+str(columns[5])+'\n')
                                    Bolean =-100
                                    Num_non_selected=Num_non_selected+1
                                    contador_fracturas+=1
                            if float(Numb_fractures_readed)%500000==0:
                                print(str(float(Numb_fractures_readed)/float(Numb_fractures)*100)+" % readed")
                            else:
                                a=0
                            if float(Numb_fractures_readed)%50000==0:
                                print( str(Numb_fractures_readed)+" fractures readed"+' of '+ str(Numb_fractures) )
                            else:
                                a=0
                                '''
                            if float(Numb_fractures_readed)>=700000:
                                print( str(Numb_fractures_readed)+" fractures readed"+' of '+ str(Numb_fractures) )
                                print( "-----------------Fractures selected "+str(float(Num_selected)))
                            else:
                                a=0
                                '''
                        else:
                            if columns[0]== str(0):
                                qq= "COORDINATES SECTION"
                                #print(str(columns[1]))
                                #init=-99999999999999
                                if int(Numb_fractures_readed)<=int(Numb_fractures):
                                    init=-99999999999999
                                else:
                                    kk=0
                                current_line=current_line+1
    #                            if current_line%100000==0:
    #                                print("current fracture is "+ str(current_line)+' of '+ str(Numb_fractures))
                                #endtime =time.time()
                                #print("time is "+str(first_start_time-endtime))
                                #print("time is "+str(first_start_time-endtime))
    #                            else:
    #                                asd=0
                            else:
                                qq=0
                            if Bolean ==100:
                                wselected.write(line+'\n')
                            else:
                                q=0
                                wdiscarted.write(line+'\n')
                else:
                    kk=0
            else:
                y=0
        wselected.write('BEGIN TESSFRACTURE'+'\n')
        wselected.write('END TESSFRACTURE'+'\n')    
        wselected.write('BEGIN ROCKBLOCK'+'\n')
        wselected.write('END ROCKBLOCK'+'\n')   
        wdiscarted.write('BEGIN TESSFRACTURE'+'\n')
        wdiscarted.write('END TESSFRACTURE'+'\n')    
        wdiscarted.write('BEGIN ROCKBLOCK'+'\n')
        wdiscarted.write('END ROCKBLOCK'+'\n')   
        print("ENDING "+fileName)
        print("SELECTED for a threshold of "+str(threshold)+" "+str(Num_selected)+" fractures")
        print("NON SELECTED for a threshold of "+str(threshold)+" "+str(Num_non_selected)+" fractures")
        #f.close()
        wselected.close()
        wdiscarted.close()
        #print(PropStore)
