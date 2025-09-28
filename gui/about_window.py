import wx
import webbrowser

class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="O programie", size=(500, 400))
        
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        title = wx.StaticText(panel, label="Shoper Sitemap Explorer")
        title_font = title.GetFont()
        title_font.SetPointSize(16)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        
        info_text = """Wersja: 1.0
        
Program służy do szybkiego pobierania Sitemap ze sklepów Shoper.
Umożliwia pobieranie na dysk głównej sitemapy oraz wybranych kategorii podsitemap.

Autor: Piotr Walczak"""
        
        info_label = wx.StaticText(panel, label=info_text)
        
        website_text = wx.StaticText(panel, label="Strona autora:")
        self.website_link = wx.StaticText(panel, label="https://pwalczak.net")
        
        self.website_link.SetForegroundColour(wx.Colour(0, 0, 255))  # Blue link
        font = self.website_link.GetFont()
        font.SetUnderlined(True)
        self.website_link.SetFont(font)
        self.website_link.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        
        self.website_link.Bind(wx.EVT_LEFT_UP, self.on_website_click)
        
        close_btn = wx.Button(panel, wx.ID_OK, label="Zamknij")
        
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(info_label, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(website_text, 0, wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add(self.website_link, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        main_sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(main_sizer)
        
        self.Center()
    
    def on_website_click(self, event):
        try:
            webbrowser.open("https://pwalczak.net")
        except Exception as e:
            wx.MessageBox(f"Nie można otworzyć strony: {e}", "Błąd", wx.OK | wx.ICON_ERROR)