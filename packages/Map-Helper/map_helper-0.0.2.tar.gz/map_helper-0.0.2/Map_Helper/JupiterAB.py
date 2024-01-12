#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all the necessary libraries. Note Haversine, Selenium
from win32com.client import Dispatch, GetActiveObject
import pythoncom
import os

import pandas as pd
import haversine as hs
import matplotlib.pyplot as plt
from haversine import Unit

#import the libraries for opening and saving the FIRMette
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import urllib


# In[2]:


#Create function to calculate distances for later on
dist_list = []
def distance(center, coords):
    dist_list.clear()
    for i in coords:
        result = hs.haversine(center,i,unit=Unit.FEET)
        dist_list.append(result)
    
    return dist_list


# In[17]:


#Create site names for DDD, store in Dataframe imported from excel doc for now
def dataRetriever():
    getFile = input(r'Paste path to excel Input file, or press Return to open one:')
    xl = Dispatch("Excel.Application")
    xl.DisplayAlerts = False
    if getFile =="":
        xl.Visible = True
        headers = ['Site','Latitude, Start','Longitude, Start','Latitude, End','Longitude, End']   
        getFile = os.getcwd() + '\Input.xlsx'
        wb = xl.Workbooks.Add()
        sheet = xl.Worksheets(1)
        sheet.Range(sheet.Cells(1,1), sheet.Cells(1,len(headers))).Value = headers
        wb.SaveAs(getFile)
        while (True):
            try:
                xl = GetActiveObject('Excel.Application')
                wb = xl.Workbooks('Input.xlsx')
            except AttributeError:
                pass
            except pythoncom.com_error as e:
                x = getattr(e, 'message', str(e))
                if "Exception occurred." in x:
                    break
                else:
                    pass
    else:
        xl.Visible = False
        wb = xl.Workbooks.Open(getFile)
        xl.Close()
    return getFile


# In[4]:


def sortData(getFile):
    df = pd.read_excel(getFile)
    df['SiteName'] = ""
    
    df.loc[pd.isnull(df.loc[:, 'Latitude, End']), 'SiteName'] = 'Site ' + df['Site'].astype(str) + " (" + round(df['Latitude, Start'], 6).astype(str) + ',' + round(df['Longitude, Start'], 6).astype(str) + ')'
    df.loc[pd.notnull(df.loc[:, 'Latitude, End']), 'SiteName'] = 'Site ' + df['Site'].astype(str) + ' (Start: ' + round(df['Latitude, Start'], 6).astype(str) + ',' + round(df['Longitude, Start'], 6).astype(str) + "; End: " + round(df['Latitude, End'], 6).astype(str) + ',' + round(df['Longitude, End'], 6).astype(str) + ')'
    
    df2 = pd.DataFrame(columns=['Name','Latitude','Longitude','Icon','Folder'])
    #Iterates through rows of excel doc and converts information into things usable by Pandas, Earthpoint
    for index, row in df.iterrows():
        #Place coordinates into dataframe
        latitudeS = str(round(row['Latitude, Start'], 6))
        longitudeS = str(round(row['Longitude, Start'],6))
        latitudeE = str(round(row['Latitude, End'],6))
        longitudeE = str(round(row['Longitude, End'],6))
        
        #Divides into start and end points, if applicable.
        if pd.notnull(row.loc['Latitude, End']):
            name = 'Site ' + str(row['Site']) + ", Start (" + latitudeS + ',' + longitudeS + ')'
            name2 = 'Site ' + str(row['Site']) + ", End (" + latitudeE + ',' + longitudeE + ')'
            df3  = pd.DataFrame([[name, latitudeS, longitudeS]],
                                columns = ['Name','Latitude','Longitude'])
            df4  = pd.DataFrame([[name2, latitudeE, longitudeE]],
                                columns = ['Name','Latitude','Longitude'])
            df2 = pd.concat([df2,df3], sort=False)
            df2 = pd.concat([df2,df4], sort=False)
        else: 
            name = 'Site ' + str(row['Site']) + " (" + latitudeS + ',' + longitudeS + ')'
            df3  = pd.DataFrame([[name, latitudeS, longitudeS]],
                                columns = ['Name','Latitude','Longitude'])
            df2 = pd.concat([df2,df3], sort=False)
            
    #converts strings into floats, resets df2 index
    df2['Latitude'] = pd.to_numeric(df2['Latitude'], downcast ="float")
    df2['Longitude'] = pd.to_numeric(df2['Longitude'], downcast ="float")
    df2 = df2.reset_index(drop=True)
    #creates coords lists for distance function
    coords = df2[['Latitude','Longitude']]
    coords = list(coords.itertuples(index=False, name=None))
    
    #finds centerpoint of group
    x = df2['Latitude'].mean()
    y = df2['Longitude'].mean()
    center1=(x,y)
    #creates dataframe for centerpoints, adds centerpoint
    dfc = pd.DataFrame([[x, y]],
                       columns = ['Latitude','Longitude'])
    #creates dataframe to store distances from centerpoints
    dfd = pd.DataFrame()
    #runs centerpoint through distance function, returns results to above dfd dataframe
    dfd['Distance1'] = distance(center1, coords)
    #distance column added to df2 to record minimun distance to centerpoint
    df2['Distance'] = dfd['Distance1']
    #folder column added to group points to nearest centerpoints
    df2['Folder'] = 'Group 1'
    dfc['Folder'] = 'Group 1'
    
    i = 1
    while (df2['Distance'] > 1500).any():
    
        #Drop out temp center points that are already in groups
        dfx = df2['Distance'] < 1500
        indices = []
        dfd2 = pd.DataFrame()
        for q in range(len(dfx)):
            if dfx[q] == True:
                indices.append(q)
        dfd2 = dfd.drop(indices) 
        #Sum and find average distance of points from centers
        dfd2['sum'] = dfd2.sum(axis=1)
        dfd2['avg'] = dfd2['sum']/(i)
        #load point that is farthest avg distance from centers
        x = df2.iloc[dfd2['avg'].idxmax(), 1]
        y = df2.iloc[dfd2['avg'].idxmax(), 2]
        tempCenter = (x,y)
        #add row to column using loaded point as temporary center for distances
        dist2 = 'Distance' + str(i+1)
        dfd[dist2] = distance(tempCenter, coords)
        #sort into groups based on distances
        df2['Folder'] = dfd.idxmin(axis = 1)
        #reset center dataframe
        dfc = pd.DataFrame()
        dfc['Latitude'] = df2.groupby('Folder')['Latitude'].mean()
        dfc['Longitude'] = df2.groupby('Folder')['Longitude'].mean()
        #reset dfd dataframe for next run
        dfd = pd.DataFrame()
        #recalculate distances from new centerpoints
        for index, row in dfc.iterrows():
            x2 = row['Latitude']
            y2 = row['Longitude']
            center2 = (x2,y2)
            dfd[index] = distance(center2, coords)
        #reload into df2, re-check if it fits into maps
        df2['Distance'] = dfd.min(axis = 1)
        i+= 1
        
    df2['Folder'] = df2['Folder'].replace({'Distance' : 'Group '},regex=True)
    
    #gives groups unique pin colors, unless there is more than 10
    if df2['Folder'].str.contains('Group 10').any():
        df2['Icon'] = '111'
    else:
        df2['Icon'] = df2['Folder'].replace({'Group ' : '11'},regex=True)
    df2 = df2.drop(columns=['Distance'])
    dfddd = pd.DataFrame(df['SiteName'])
    dfc = dfc.reset_index()
    try:
        dfc['Folder'] = dfc['Folder'].replace({'Distance' : 'Group '},regex=True)
    except KeyError:
        raise Warning('Please enter data into Input file and restart')
    
    return dfddd, df2, dfc


# In[5]:


def printTheMasks(df2, dfc):
    labelmaker = input('Add labels to FIRMette masks? (y/n)')
    for i, row in dfc.iterrows():
        #loads points for each group, and grabs the center point.
        group = row['Folder']
        xs = list(df2.loc[df2['Folder']==group,'Latitude'])
        ys = list(df2.loc[df2['Folder']==group,'Longitude'])
        xcen = float(dfc.loc[i,'Latitude']) #literally just use row['Latitude'], dumb ass
        ycen = float(dfc.loc[i,'Longitude']) #same
        xs.append(xcen)
        ys.append(ycen)
        #setting the dimensions for the eventual plot. This was a stupid way to do this probs, but it works.
        yx = ycen-.00475
        yr = ycen+.00475
        xx = xcen-.00373
        xr = xcen+.00373
        
        #I don't understand how GPS coordinates map to Euclidean plains, and at this point it's too late to learn
        #I know x/y are backwards, and have been this whole time, but I didn't realize until here. It's easier this way.
        #But generally, this maps the points to a scatter plot and gets the plot formatted
        fig, ax = plt.subplots()
        ax.scatter(ys,xs)
        ax.set_xlim((yx,yr))
        ax.set_ylim((xx,xr))
        x0,x1 = ax.get_xlim()
        y0,y1 = ax.get_ylim()
        ax.set_aspect(abs(x0-x1)/abs(y0-y1))
        ax.scatter(ys,xs)
        plt.axis('off')
        
        #Creates labels for the FIRMette, if y was selected above.
        if labelmaker == 'y':
            #Works~But not quite the way I want it to
            n = list(df2.loc[df2['Folder']==group,'Name'])
            for i, txt in enumerate(n):
                ax.annotate(txt, (ys[i],xs[i]), 
                            xytext=(30,30), textcoords ='offset points', 
                            bbox=dict(boxstyle='square', fc='w'),
                            arrowprops = dict(arrowstyle='wedge',relpos=(0.,0.),connectionstyle='arc3',fc='tab:orange'))
                
        #print masks to the same folder
        fig.set_size_inches(13,11.5)
        fig.savefig(group,bbox_inches='tight',pad_inches=0,transparent=True)
        plt.close(fig)


# In[6]:


def printTheMaps(dfc):
    printmaker = input('Print FIRMette PDFs? (y/n)')
    if printmaker == 'y':
        for i, row in dfc.iterrows():
            #Use Selenium to initiate an Edge browser and download corresponding FIRMette
            driver = webdriver.Edge()
            url = 'https://msc.fema.gov/portal/firmette?latitude='+str(row['Latitude'])+'&longitude='+str(row['Longitude'])
            driver.get(url)
            WebDriverWait(driver, 10)
            WebDriverWait(driver, 60).until(lambda driver: driver.current_url != url)
            if driver.current_url.endswith('.pdf'):
                pdf_url = driver.current_url
                driver.get(pdf_url)
                group = row['Folder']
                name = group + '.pdf'
                urllib.request.urlretrieve(pdf_url, name)
                driver.close()
            else:
                print('No map for' + group)
                driver.close()   


# In[19]:


def Printer(dataf):
    fileName = input('Unique file name?')
    if 'SiteName' in dataf.columns:
        if fileName == '':
            fileName = 'DDD_Names.xlsx'
        else:
            fileName = fileName + '.xlsx'
        dataf.to_excel(fileName)
    elif 'Name' in dataf.columns:
        if fileName == '':
            fileName = 'Earthpoint.xlsx'
        else:
            fileName = fileName + '.xlsx'
        dataf.to_excel(fileName)


# In[10]:


def JupiterAB():
    Data = dataRetriever()
    DDD, Earthpoint, Centers = sortData(Data)
    printOut = input('Print: DDD, EP, FIRM? ')
    while (True):
        try:
            if printOut == 'DDD' or printOut == 'd':
                Printer(DDD)
            elif printOut == 'EP' or printOut == 'e':
                Printer(Earthpoint)
            elif printOut == 'FIRM' or printOut == 'f':
                printTheMasks(Earthpoint, Centers)
                printTheMaps(Centers)
            elif printOut == 'QUIT' or printOut == 'q':
                try:
                    os.remove('Input.xlsx')
                except:
                    pass
                break
            else:
                raise Exception
            printOut = input("Print again: DDD, Earthpoint, FIRM? ")
            pass
        except:
            printOut = input('Please enter a valid print: DDD, Earthpoint, FIRM? ')
            pass
        
if __name__ == "__main__":
    JupiterAB()
