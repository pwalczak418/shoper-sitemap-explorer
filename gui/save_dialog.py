import wx

class SaveDialog:
    def save_file_dialog(self):

        with wx.FileDialog(
            None, 
            "Wybierz miejsce zapisu pliku", 
            wildcard="Plik XML (*.xml)|*.xml|Wszystkie pliki (*.*)|*.*",
            defaultFile="sitemap.xml", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_OK:
                # Returning chosen file path
                return fileDialog.GetPath()
            else:
                return None
        
    def choose_folder_dialog(self):
        with wx.DirDialog(
            None, 
            "Wybierz folder docelowy", 
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
            
            if dirDialog.ShowModal() == wx.ID_OK:
                # Returning chosen folder path
                return dirDialog.GetPath()
            else:
                return None