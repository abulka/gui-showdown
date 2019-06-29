# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"My ECS demo", pos = wx.DefaultPosition, size = wx.Size( 486,360 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetBackgroundColour( wx.Colour( 255, 255, 135 ) )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer5.Add( self.m_staticText1, 1, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MyLabel lkjsd lkjkljs d sdkfjfsdljflskdjf", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( 100 )

		self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		self.m_staticText2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		bSizer5.Add( self.m_staticText2, 1, wx.ALL, 5 )


		self.m_panel1.SetSizer( bSizer5 )
		self.m_panel1.Layout()
		bSizer5.Fit( self.m_panel1 )
		bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Welcome Message (model)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.m_textCtrl1, 1, wx.ALL, 5 )


		bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"User (model)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer3.Add( self.m_textCtrl2, 1, wx.ALL, 5 )

		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer3.Add( self.m_textCtrl3, 1, wx.ALL, 5 )


		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

		self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Change case of welcome message (via model)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox1, 0, wx.ALL, 5 )

		self.m_checkBox1A = wx.CheckBox( self, wx.ID_ANY, u"Change case of welcome message (display only, not via model)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox1A, 0, wx.ALL, 5 )

		self.m_checkBox2 = wx.CheckBox( self, wx.ID_ANY, u"Change case of top right message", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox2, 0, wx.ALL, 5 )

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Reset Welcome Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button1, 0, wx.ALL, 5 )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Reset User", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button3, 0, wx.ALL, 5 )

		self.m_button_rendernow = wx.Button( self, wx.ID_ANY, u"Render Now", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE )
		bSizer1.Add( self.m_button_rendernow, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_textCtrl1.Bind( wx.EVT_TEXT_ENTER, self.onEnter )
		self.m_textCtrl2.Bind( wx.EVT_TEXT_ENTER, self.onEnterUserName )
		self.m_textCtrl3.Bind( wx.EVT_TEXT_ENTER, self.onEnterUserSurname )
		self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.onCheck1 )
		self.m_checkBox1A.Bind( wx.EVT_CHECKBOX, self.onCheckToggleWelcomeOutputsOnly )
		self.m_checkBox2.Bind( wx.EVT_CHECKBOX, self.onCheck2 )
		self.m_button1.Bind( wx.EVT_BUTTON, self.onResetWelcome )
		self.m_button3.Bind( wx.EVT_BUTTON, self.onClickResetUser )
		self.m_button_rendernow.Bind( wx.EVT_BUTTON, self.onClickRenderNow )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onEnter( self, event ):
		event.Skip()

	def onEnterUserName( self, event ):
		event.Skip()

	def onEnterUserSurname( self, event ):
		event.Skip()

	def onCheck1( self, event ):
		event.Skip()

	def onCheckToggleWelcomeOutputsOnly( self, event ):
		event.Skip()

	def onCheck2( self, event ):
		event.Skip()

	def onResetWelcome( self, event ):
		event.Skip()

	def onClickResetUser( self, event ):
		event.Skip()

	def onClickRenderNow( self, event ):
		event.Skip()


