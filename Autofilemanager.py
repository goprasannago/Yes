import os
import shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView

FILE_TYPE_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.docx', '.doc', '.txt'],
    'Audio': ['.mp3', '.wav', '.aac', '.m4a'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Compressed': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.sh', '.bat'],
    'Pdfdocuments': ['.pdf'],
    'Presentations': ['.pptx'],
    'Accountings': ['.xls', '.xlsx'],
    'WebFiles': ['.html', '.css', '.js','.php'],
    'Datafiles': ['.csv', '.json', '.xml'],
    'Databases': ['.db', '.sql'],
    'Others': []
}

def get_folder_for_file(extension):
    for folder, ext_list in FILE_TYPE_MAP.items():
        if extension.lower() in ext_list:
            return folder
    return 'Others'

class FileOrganizerApp(App):
    def build(self):
        self.selected_dir = ""
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.btn_select = Button(text="Select Folder", size_hint_y=None, height=40)
        self.btn_select.bind(on_press=self.open_filemanager)
        self.btn_organize = Button(text="Organize Files!", size_hint_y=None, height=50)
        self.btn_organize.bind(on_press=self.organize_files)
        self.log = Label(size_hint_y=None, height=300, text="", halign="left", valign="top")
        self.log.bind(texture_size=self.adjust_log_height)
        self.scroll = ScrollView(size_hint=(1, None), size=(800, 300))
        self.scroll.add_widget(self.log)
        self.layout.add_widget(self.btn_select)
        self.layout.add_widget(self.btn_organize)
        self.layout.add_widget(self.scroll)
        return self.layout

    def adjust_log_height(self, instance, value):
        self.log.height = value[1]

    def open_filemanager(self, instance):
        # Only add widgets to one parent: popup_content
        filechooser = FileChooserListView(path='.', dirselect=True, size_hint=(1, 0.9))
        btn_ok = Button(text="OK", size_hint=(1, 0.1))
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(filechooser)
        popup_content.add_widget(btn_ok)

        popup = Popup(title="Choose a Folder", content=popup_content, size_hint=(0.9, 0.8))
        btn_ok.bind(on_press=lambda x: self.select_folder(filechooser, popup))
        popup.open()

    def select_folder(self, filechooser, popup):
        sel = filechooser.selection
        if sel:
            self.selected_dir = sel[0]
            self.log.text += f"\nSelected directory: {self.selected_dir}"
        else:
            self.log.text += "\nNo folder selected!"
        popup.dismiss()

    def organize_files(self, instance):
        if not self.selected_dir:
            self.log.text += "\nNo folder selected!"
            return
        count = 0
        try:
            for filename in os.listdir(self.selected_dir):
                file_path = os.path.join(self.selected_dir, filename)
                if os.path.isfile(file_path):
                    _, extension = os.path.splitext(filename)
                    folder_name = get_folder_for_file(extension)
                    category_folder = os.path.join(self.selected_dir, folder_name)
                    os.makedirs(category_folder, exist_ok=True)
                    if file_path != os.path.join(category_folder, filename):
                        shutil.move(file_path, os.path.join(category_folder, filename))
                        self.log.text += f"\nMoved: {filename} to {folder_name}"
                        count += 1
            self.log.text += f"\nTotal files moved: {count}"
        except Exception as e:
            self.log.text += f"\nError: {e}"

if __name__ == "__main__":
    FileOrganizerApp().run()
