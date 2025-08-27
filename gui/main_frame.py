import wx
from utils.url_validator import Validator
from gui.about_window import AboutDialog
from gui.save_dialog import SaveDialog
from core.sitemap_downloader import SitemapDownloader

class MainFrame(wx.Frame):
    def __init__(self, title="Shoper Sitemap Explorer"):
        super().__init__(parent=None, title=title, size=(800,500))

        self.downloader = SitemapDownloader()

        self.set_icon()

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        url_box = wx.StaticBox(main_panel, label="Konfiguracja URL")
        url_sizer = wx.StaticBoxSizer(url_box, wx.VERTICAL)
        
        url_label = wx.StaticText(main_panel, label="Podaj adres URL:")
        self.url_text = wx.TextCtrl(main_panel, style=wx.TE_PROCESS_ENTER)
        
        url_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.select_url_btn = wx.Button(main_panel, label="Zatwierdź")
        self.change_url_btn = wx.Button(main_panel, label="Zmień")
        self.change_url_btn.Enable(False)
        
        url_buttons_sizer.Add(self.select_url_btn, 0, wx.RIGHT, 5)
        url_buttons_sizer.Add(self.change_url_btn, 0)
        
        url_sizer.Add(url_label, 0, wx.ALL, 5)
        url_sizer.Add(self.url_text, 0, wx.ALL | wx.EXPAND, 5)
        url_sizer.Add(url_buttons_sizer, 0, wx.ALL | wx.CENTER, 5)
        
        ###

        sitemap_box = wx.StaticBox(main_panel, label="Operacje Sitemap")
        sitemap_sizer = wx.StaticBoxSizer(sitemap_box, wx.VERTICAL)
        
        self.main_sitemap_btn = wx.Button(main_panel, label="Pobierz główną Sitemapę")
        
        childsitemap_label = wx.StaticText(main_panel, label="Pobierz podsitemapy:")
        
        self.options = ["Produkty", "Kategorie", "Producenci", "Blog", "Strony informacyjne", "Kolekcje"]
        
        self.checkboxes = {}
        checkbox_sizer = wx.FlexGridSizer(3, 2, 5, 10)
        
        for option in self.options:
            checkbox = wx.CheckBox(main_panel, label=option)
            self.checkboxes[option] = checkbox
            checkbox_sizer.Add(checkbox, 0, wx.EXPAND)
        

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.select_all_btn = wx.Button(main_panel, label="Wszystkie")
        self.childsitemap_btn = wx.Button(main_panel, label="Pobierz podsitemapy")
        
        buttons_sizer.Add(self.select_all_btn, 0, wx.RIGHT, 5)
        buttons_sizer.Add(self.childsitemap_btn, 0)
        
        sitemap_sizer.Add(self.main_sitemap_btn, 0, wx.ALL | wx.EXPAND, 5)
        sitemap_sizer.Add(childsitemap_label, 0, wx.ALL, 5)
        sitemap_sizer.Add(checkbox_sizer, 0, wx.ALL | wx.EXPAND, 5)
        sitemap_sizer.Add(buttons_sizer, 0, wx.ALL | wx.CENTER, 5)
        
        self.sitemap_panel_items = [
            self.main_sitemap_btn, self.childsitemap_btn, 
            self.select_all_btn
        ]
        self.sitemap_panel_items.extend(list(self.checkboxes.values()))
        self.enable_sitemap_section(False)
        
        # Footer with "About" button
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.about_btn = wx.Button(main_panel, label="O programie")
        bottom_sizer.Add(wx.StaticText(main_panel), 1)
        bottom_sizer.Add(self.about_btn, 0, wx.ALL, 5)
        

        main_sizer.Add(url_sizer, 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(sitemap_sizer, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        main_panel.SetSizer(main_sizer)
        

        # Button & checkboxes handlers
        self.select_url_btn.Bind(wx.EVT_BUTTON, self.on_select_url)
        self.change_url_btn.Bind(wx.EVT_BUTTON, self.on_change_url)
        self.url_text.Bind(wx.EVT_TEXT_ENTER, self.on_select_url)
        
        self.main_sitemap_btn.Bind(wx.EVT_BUTTON, self.on_mainsitemap_download)
        self.childsitemap_btn.Bind(wx.EVT_BUTTON, self.on_childsitemap_download)
        self.select_all_btn.Bind(wx.EVT_BUTTON, self.on_off_all)
        self.about_btn.Bind(wx.EVT_BUTTON, self.on_about)
        
        for checkbox in self.checkboxes.values():
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)
        

        self.Center()
        self.Show()

    # METHODS

    def enable_sitemap_section(self, enable):
        """Sitemap options are disabled before URL validation"""
        for item in self.sitemap_panel_items:
            item.Enable(enable)
    
    def on_select_url(self, event):
        url = self.url_text.GetValue().strip()
        
        if not url:
            wx.MessageBox("Proszę podać adres URL", "Błąd", wx.OK | wx.ICON_ERROR)
            return
        
        validated_url = self.on_validate(url)

        if not validated_url:
            wx.MessageBox("Nie udało się połączyć ze sklepem Shoper", "Błąd", wx.OK | wx.ICON_ERROR)
            return

        self.url = validated_url
        
        self.select_url_btn.Enable(False)
        self.change_url_btn.Enable(True)
        self.url_text.Enable(False)
        self.enable_sitemap_section(True)
        
        wx.MessageBox(f"URL zatwierdzony: {self.url}", "Sukces", wx.OK | wx.ICON_INFORMATION)
    
    def on_change_url(self, event):
        self.select_url_btn.Enable(True)
        self.change_url_btn.Enable(False)
        self.url_text.Enable(True)
        self.enable_sitemap_section(False)
        self.url_text.SetFocus()
    
    def on_mainsitemap_download(self, event):
        savedialog = SaveDialog()
        returned_path = savedialog.save_file_dialog()
        if not returned_path:
            wx.MessageBox("Anulowano.", "Błąd", wx.OK | wx.ICON_ERROR)
            return
        if self.downloader.download_mainsitemap(self.url, returned_path):
            wx.MessageBox(f"Pobrano Sitemapę do {returned_path}", "Sukces", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Wystąpił niespodziewany błąd podczas zapisu Sitemapy. Spróbuj ponownie.", "Błąd", wx.OK | wx.ICON_ERROR)
    
    def on_childsitemap_download(self, event):
        selected = [option for option, checkbox in self.checkboxes.items() if checkbox.GetValue()]
        
        if not selected:
            wx.MessageBox("Proszę wybrać co najmniej jedną opcję.", "Błąd", wx.OK | wx.ICON_ERROR)
            return
        
        url = self.url_text.GetValue()
        selected_str = ", ".join(selected)
        print(f"Wybrano następujące podmapy: {selected_str}")
        wx.MessageBox("Ta funkcja zostanie wkrótce zaimplementowana", "Błąd", wx.OK | wx.ICON_ERROR)
        return
    
    def on_off_all(self, event):
        all_selected = all(checkbox.GetValue() for checkbox in self.checkboxes.values())
        
        if all_selected:
            for checkbox in self.checkboxes.values():
                checkbox.SetValue(False)
            self.select_all_btn.SetLabel("Wszystkie")
        else:
            for checkbox in self.checkboxes.values():
                checkbox.SetValue(True)
            self.select_all_btn.SetLabel("Żadne")
    
    def on_checkbox_change(self, event):

        all_selected = all(checkbox.GetValue() for checkbox in self.checkboxes.values())
        
        if all_selected:
            self.select_all_btn.SetLabel("Żadne")
        else:
            self.select_all_btn.SetLabel("Wszystkie")
    
    def on_about(self, event):
        dialog = AboutDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def set_icon(self):
        try:
            icon = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
        except:
            print("Nie znaleziono ikony")

    def on_validate(self, url):

        validator = Validator()
        validated_url = validator.validate_url(url)

        if validated_url and validator.connect(validated_url):
            return validated_url
        else:
            return False