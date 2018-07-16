# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class FrmMain
###########################################################################

class FrmMain(wx.Frame):
	
	def __init__(self, parent):
		wx.Frame.__init__ (
            self, parent, id = wx.ID_ANY, title = u"GetRoute - Exams version 0.9",
            pos = wx.DefaultPosition, size = wx.Size( 450,197 ),
            style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL
        )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		gSizer2 = wx.GridSizer( 1, 2, 0, 0 )
		
		fgSizer3 = wx.FlexGridSizer( 5, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Locality A", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer3.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		self.tctrl_A = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer3.Add( self.tctrl_A, 0, wx.ALL, 5 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Waypoint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		fgSizer3.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.tctrl_WP1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer3.Add( self.tctrl_WP1, 0, wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Waypoint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer3.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.tctrl_WP2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer3.Add( self.tctrl_WP2, 0, wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Locality B", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		fgSizer3.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.tctrl_B = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		fgSizer3.Add( self.tctrl_B, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( ( 0, 25), 1, wx.EXPAND, 5 )
		
		
		gSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		self.btn_create_route = wx.Button( self, wx.ID_ANY, u"Create route", wx.DefaultPosition, wx.Size( 205,120 ), 0 )
		gSizer2.Add( self.btn_create_route, 0, wx.ALL, 5 )
		
		
		self.SetSizer( gSizer2 )
		self.Layout()
		self.stbar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre(wx.BOTH)
	
	def __del__(self):
		pass
