#!/usr/bin/env python3
#
# Скрипт для определения маршрута движения автомобиля между N ≤ 4 точек. 
# Входная информация (наименования городов\населенных пунктов), вывод должен содержать:
# координаты всех внесенных точек;
# дистанцию на маршруте в км;
# ориентировочное время в пути;
#
# A script for seartching car route between <=4 localities
#
# Copyright (C) 2018 dx-77 <d.x77@yandex.ru>.
# GitHub : https://github.com/dx-77
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import googlemaps
import requests
import wx
import ui

ROUTE_URL = 'https://maps.googleapis.com/maps/api/directions/json'

KEY = 'AIzaSyDQ033vdji13ejN4lzFEB1NN8HLg8-1HTA'


class MyWin(ui.FrmMain):
    def __init__(self, parent):
        self.gmaps = googlemaps.Client(key=KEY)
        self.params = {'mode': 'driving',
          'origin': '',
          'waypoints': '',
          'destination': '',
          'key': KEY}

        ui.FrmMain.__init__(self, parent)
          
        self.Centre(wx.BOTH)
        self.SetBackgroundColour(wx.NullColour)
        
        self.btn_create_route.Bind(wx.EVT_BUTTON, self.btn_create_route_click)
             

    def getcoords(self, locality):
        coords = []
        f_addresses = []

        for l in locality:
            gr = self.gmaps.geocode(l)
            if gr:
                f_addresses.append(gr[0]['formatted_address'])
                lng = gr[0]['geometry']['location']['lng']
                lat = gr[0]['geometry']['location']['lat']
                coords.append(str(lng) + ',' + str(lat))

        return [f_addresses, coords]
    

    def btn_create_route_click(self, event):
        self.btn_create_route.Disable()

        A = self.tctrl_A.Value.strip()
        WP1 = self.tctrl_WP1.Value.strip()
        WP2 = self.tctrl_WP2.Value.strip()
        B = self.tctrl_B.Value.strip()
        locality = [i for i in (A, WP1, WP2, B) if i]
        if not A or not B:
            self.btn_create_route.Enable()
            dlg = wx.MessageDialog(self, 'Input localities A and B !',
                                   'Attention', wx.ICON_EXCLAMATION | wx.OK)
            dlg.ShowModal()
            return

        f_addresses, coords = self.getcoords(locality)
        
        self.stbar.SetStatusText('Creating the route...')
        info = []
        for i in range(len(f_addresses)):
            info.append('"%s" (%s)' % (f_addresses[i], coords[i]))

                  
        self.params['origin'] = f_addresses[0]
        self.params['destination'] = f_addresses[-1]

        if WP1 and WP2:
            WP1 = f_addresses[1] + '|via:' + f_addresses[2]
        elif WP2:
            WP1 = f_addresses[1]
        if WP1:
            self.params['waypoints'] = 'via:' + WP1
        
        res = requests.get(ROUTE_URL, params=self.params)
        if res.status_code == requests.codes.ok:
            res = res.json()
            info.append(res['routes'][0]['legs'][0]['distance']['text'])
            info.append(res['routes'][0]['legs'][0]['duration']['text'])
            info = '\n'.join(info)
            dlg = wx.MessageDialog(self, info, 'Route', wx.OK)
            dlg.ShowModal()
        else:
            dlg = wx.MessageDialog(self, 'Cannot open URL %s' % ROUTE_URL,
                                   'Attention', wx.ICON_EXCLAMATION | wx.OK)
            dlg.ShowModal()
    
        self.stbar.SetStatusText('')
        self.btn_create_route.Enable()


def main():
    app = wx.App()
    wnd = MyWin(None)
    wnd.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
