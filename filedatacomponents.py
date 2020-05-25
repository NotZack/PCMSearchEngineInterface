from kivy.uix.floatlayout import FloatLayout

'''
The room data components of the app
'''


class FileDataComponents(FloatLayout):

    file_data = None
    current_view = None

    def __init__(self, **kwargs):
        super(FileDataComponents, self).__init__(**kwargs)

        self.current_view = FloatLayout()

        self.add_widget(self.current_view)

    # Calls for the creation of room data components
    def show_file_data(self, query_results):
        self.file_data = self.parse_query_results(query_results)
        self.create_file_stats()

    # Creates and displays the room data component components
    def create_file_stats(self):
        self.destroy_current_view()
        self.current_view.add_widget(FileView(self.file_data))
        self.current_view.add_widget(FileInformation(self.file_data))
        self.current_view.add_widget(FileInformation.session_view)

    # Destroys any previous room data display
    def destroy_current_view(self):
        self.remove_widget(self.current_view)
        FileInformation.session_view = FloatLayout()

        self.current_view = FloatLayout()
        self.add_widget(self.current_view)

    # Parses raw query results into an array where each result is its own element
    @staticmethod
    def parse_query_results(raw_data):
        outer_array = []
        for result in raw_data.split(','):
            outer_array.append(result)

        return outer_array


'''
The component that displays the selected file
'''


class FileView(FloatLayout):

    def __init__(self, data, **kwargs):
        super(FileView, self).__init__(**kwargs)

        self.create_plasma_cam_view()

    def create_plasma_cam_view(self):
        print("here")
        print("here2")


'''
The view of room and session specific information
'''


class FileInformation(FloatLayout):

    session_view = FloatLayout()

    def __init__(self, data, **kwargs):
        super(FileInformation, self).__init__(**kwargs)

        self.create_file_information_view(data)

    def create_file_information_view(self, data):
        print("here")
        print("here2")

    @staticmethod
    def create_session_information_view(data):
        FileInformation.session_view.clear_widgets()
