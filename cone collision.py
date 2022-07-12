# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:32:45 2021

@author: anmorrow, modified matlab code from rgutti
"""
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_VARS = {'window': False}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all') 


AppFont = 'Any 16'
sg.theme('LightGrey')

layout = [[sg.Text("Isocenter position [mm].  If not localized, AP = Y, Lat = X, Vert = Z")],
        [sg.Text("AP",size=(4,0)),
           sg.Text("Lat",size=(3,0)),
           sg.Text("Vert",size=(4,0))],
          
          [sg.InputText(size=(4,0)),
          sg.InputText(size=(4,0)),
          sg.InputText(size=(4,0))],
          
          [sg.Text("Sterotactic origin(easy way: put a distance marker at 12cm above the table, centered L-R, 2.2cm inferior to the middle mask posts")],
          
          [sg.InputText('0',size=(4,0)),
          sg.InputText('0',size=(4,0)),
          sg.InputText('0',size=(4,0))],
          
          [sg.Button('Draw')],
          
          [sg.Canvas(key='figCanvas')],
          [sg.Button('Exit', font=AppFont)]]
_VARS['window'] = sg.Window('Cone Collision Check Tool',
                            layout,
                            finalize=True,
                            resizable=True,
                            element_justification="left")

surfdata=[[-10,20,-12],[-9,20,-12],[-8,20,-12],[-7,20,-12],[-6,20,-12],[-5,20,-12],[-4,20,-12],[-3,20,-12],
          [-2,20,-12],[-1,20,-12],[0,20,-12],[1,20,-12],[2,20,-12],[3,20,-12],[4,20,-12],[5,20,-12],[6,20,-12],
          [7,20,-12],[8,20,-12],[9,20,-12],[10,20,-12],[11,19,-12],[12,18,-12],[13,17,-12],[14,16,-12],[15,15,-12],
          [15,14,-12],[15,13,-12],[15,12,-12],[15,11,-12],[15,10,-12],[15,9,-12],[15,8,-12],[15,7,-12],[15,6,-12],
          [15,5,-12],[15,4,-12],[15,3,-12],[15,2,-12],[15,1,-12],[15,0,-12],[15,-1,-12],[15,-2,-12],[15,-3,-12],
          [15,-4,-12],[-15,-4,-12],[-15,-3,-12],[-15,-2,-12],[-15,-1,-12],[-15,0,-12],[-15,1,-12],[-15,2,-12],
          [-15,3,-12],[-15,4,-12],[-15,5,-12],[-15,6,-12],[-15,7,-12],[-15,8,-12],[-15,9,-12],[-15,10,-12],
          [-15,11,-12],[-15,12,-12],[-15,13,-12],[-15,14,-12],[-15,15,-12],[-14,16,-12],[-13,17,-12],[-12,18,-12],
          [-11,19,-12],[-10,20,-12]]

figure_agg=None
while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == 'Draw':
        
        if figure_agg:
            delete_figure_agg(figure_agg)
        
        event, iso = _VARS['window'].read() 
        
        isoxyz=[-0.1*(float(iso[1])-float(iso[4])),0.1*(float(iso[2])-float(iso[5])),0.1*(float(iso[0])-float(iso[3]))]
        
        couchangle1=[]
        gantryangle1=[]
        couchangle2=[]
        gantryangle2=[]
        distances=[]
        
        for i in range(len(surfdata)):
            dist=((surfdata[i][0]-isoxyz[0])**2+(surfdata[i][1]-isoxyz[1])**2+(surfdata[i][2]-isoxyz[2])**2)**0.5
            if (dist>24.5):
                theta=np.degrees(np.arccos((surfdata[i][2]-isoxyz[2])/dist))
                phi=np.degrees(np.arctan((surfdata[i][1]-isoxyz[1])/(surfdata[i][0]-isoxyz[0])))
                if (phi<0):
                    couchangle1.append(360+phi)
                    gantryangle1.append(360-theta)
                else:
                    couchangle2.append(phi)
                    gantryangle2.append(theta)
                     
        gridlines = [10*f for f in range(37)]           
                    
        fig, (ax2,ax1) = plt.subplots(1,2)
        ax1.scatter(couchangle1,gantryangle1,s=800)
        ax1.set_xlim(270,360)
        ax1.set_ylim(180,360)
        ax1.set_aspect(0.5)
        ax1.set_xlabel("Couch Angle")
        ax1.set_xticks([10*f for f in range(27,36)])
        ax1.set_yticks([10*f for f in range(18,36)])
        ax1.grid()
        
        ax2.scatter(couchangle2,gantryangle2,s=800)
        ax2.set_xlim(0,90)
        ax2.set_ylim(0,180)
        ax2.set_aspect(0.5)
        ax2.set_xlabel("Couch Angle")
        ax2.set_ylabel("Gantry Angle")
        ax2.set_xticks([10*f for f in range(0,9)])
        ax2.set_yticks([10*f for f in range(0,18)])
        ax2.grid()
        fig.set_size_inches(20,10)
        
        figure_agg=draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
_VARS['window'].close()