import wx
from gui import MyFrame1   #  <--- the wxformbuilder generated python module

class MyFrame1A(MyFrame1):
	pass

	# def OnButton1(self, event):
    #     print "button pushed"
	#
    # def OnHtml2(self, event):
    #     url = "http://www.wxpython.org/docs/api/wx.html.HtmlWindow-class.html"
    #     wx.CallAfter(frame.m_htmlWin1.LoadPage, url)
	#
    # def OnLoadHtml1(self, event):
    #     url = "http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm"
    #     wx.CallAfter(frame.m_htmlWin1.LoadPage, url)
	# frame.m_htmlWin1.LoadPage(url)


app = wx.App()
frame = MyFrame1A(None)
frame.Show()
frame.SetSize((400, 400))

app.MainLoop()
