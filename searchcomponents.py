import os

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import rootlayout
import socketcomm
from decor import ResizableLabel

'''
The components that handle specific folder selection
'''

folder_search_modify = []


class FolderSearchComponents(FloatLayout):

    def __init__(self, **kwargs):
        super(FolderSearchComponents, self).__init__(**kwargs)

        self.folder_parent_label = ResizableLabel(
            text='Base folder', size_hint=(0.2, 0.05), pos_hint={'x': 0.025, 'y': 0.90}
        )
        self.folder_overview_container = ScrollView(size_hint=(0.2, 0.25), pos_hint={'x': 0.025, 'y': 0.65})
        self.folder_overview_contents = GridLayout(cols=1, size_hint_y=None, height=2000)

        self.folder_overview_container.add_widget(self.folder_overview_contents)

        self.folder_child_label = ResizableLabel(
            text='Child folder', size_hint=(0.2, 0.05), pos_hint={'x': 0.25, 'y': 0.90}
        )
        self.folder_specific_container = ScrollView(size_hint=(0.2, 0.25), pos_hint={'x': 0.25, 'y': 0.65})
        self.folder_specific_contents = GridLayout(cols=1, size_hint_y=None, height=2000)

        self.folder_specific_container.add_widget(self.folder_specific_contents)

        self.folder_search_label = ResizableLabel(
            text="Searching folders: ", size_hint=(0.2, 0.05), pos_hint={'x': 0.025, 'y': 0.55}
        )
        self.clear_button = Button(on_press=self.clear_folder_search, text="Clear folders", size_hint=(0.05, 0.05),
                                   pos_hint={'x': 0.25, 'y': 0.55})

        self.add_widget(self.folder_parent_label)
        self.add_widget(self.folder_child_label)
        self.add_widget(self.clear_button)
        self.add_widget(self.folder_search_label)
        self.add_widget(self.folder_overview_container)
        self.add_widget(self.folder_specific_container)

        self.create_default_buttons()

    def clear_folder_search(self, button):
        folder_search_modify.clear()
        self.folder_search_label.text = "Searching folders: "

    def update_search_label(self, new_element):
        if new_element not in folder_search_modify:
            self.folder_search_label.text += new_element + ", "
            folder_search_modify.append(new_element)

    def add_folder_filter(self, button):
        self.update_search_label(button.text)

    def create_overview_contents(self, button):
        self.folder_overview_contents.clear_widgets()
        [self.folder_overview_contents.add_widget(Button(text=x, on_press=self.create_folder_specific_contents))
         for x in os.listdir(socketcomm.base_directory) if not '.' in x and not "segments_" in x]
        self.folder_overview_contents.height = 35 * len(self.folder_overview_contents.children)

    def create_folder_specific_contents(self, button):
        self.folder_specific_contents.clear_widgets()

        self.update_search_label(button.text)

        [self.folder_specific_contents.add_widget(Button(text=x, on_press=self.add_folder_filter))
         for x in os.listdir(socketcomm.base_directory + "\\" + button.text) if not '.' in x and not "segments_" in x]
        self.folder_specific_contents.height = 35 * len(self.folder_specific_contents.children)

    def create_default_buttons(self):
        folder_button = Button(text="Master Index")
        folder_button.bind(on_press=self.create_overview_contents)
        self.folder_overview_contents.height = 35

        self.folder_overview_contents.add_widget(folder_button)

        self.folder_specific_contents.height = 35
        self.folder_specific_contents.add_widget(Label(text="Choose a base folder"))


'''
The components that handle file searching
'''


class FileSearchComponents(FloatLayout):

    def __init__(self, **kwargs):
        super(FileSearchComponents, self).__init__(**kwargs)

        self.search_input = TextInput(multiline=False, size_hint=(0.20, 0.05), pos_hint={'x': 0.025, 'y': 0.45})
        self.search_input.bind(text=self.on_type)

        self.search_results_container = ScrollView(size_hint=(0.2, 0.25), pos_hint={'x': 0.025, 'y': 0.20})
        self.search_results = GridLayout(cols=1, size_hint_y=None, height=2000)

        self.search_results_container.add_widget(self.search_results)

        self.add_widget(self.search_input)
        self.add_widget(self.search_results_container)

    # Sends search input text to socket whenever anything is typing within search_input, then displays the results
    def on_type(self, instance, text):
        self.search_results.clear_widgets()

        if len(folder_search_modify) > 0:
            query_result = socketcomm.send_query_to_socket(
                self.search_input.text + " Folder_names: " + str(folder_search_modify))
        else:
            query_result = socketcomm.send_query_to_socket(self.search_input.text)

        # Splits the aggregate query result into its individual results
        if query_result is not None:
            query_split = query_result.split(',')
            self.search_results.height = len(query_split) * 35
            for data in query_split:
                if len(data) > 2:
                    result_button = Button(text=data.strip())
                    result_button.bind(on_press=self.on_file_collect)
                    self.search_results.add_widget(result_button)

    # Displays the room information of the rooms search result button
    @staticmethod
    def on_file_collect(button):
        if ("Invalid query" in button.text) or ("No results found" in button.text):
            return

        file_data = socketcomm.collect_exact_query(button.text)

        print("File data: " + file_data)
        rootlayout.root.file_data_display.show_file_data(file_data)
