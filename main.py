from functools import partial
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.clock import Clock

from everest import RosManager

BTN_SELECT_TOPIC_ID_PREFIX = "btn_select_topic_"
DROPDOWN_TOPIC_ID_PREFIX = "dropdown_topic_"
CHECKBOX_BOOL_VALUE_ID_PREFIX = "checkbox_bool_value_topic_"
CHECKBOX_PUB_CONTINUOS_ID_PREFIX = "checkbox_topic_"
update_topic_callback_chain = []

class MainPage(Widget):
    rows = NumericProperty(2)
    topic_grid_h = NumericProperty(100)
    grid_top = NumericProperty(0)
    topic_container_id_counter = 0

    def __init__(self):
        super().__init__()

    def update_topic_list(self):

        for c in update_topic_callback_chain:

            try:
                c()
            except:
                print(f"invoke callcak {c} error")

    def add_topic_container(self):

        self.add_widget(self.topic_container)

    def add_topic_container(self):

        self.rows = self.rows + 1

        # btn select topic

        grid = GridLayout(cols= 6, rows=1, size=(1000, 100), spacing=10)
        btn_select_topic_id = f"{BTN_SELECT_TOPIC_ID_PREFIX}{self.topic_container_id_counter}"
     
        btn = Button(
                     text= "Select topic",
                     size_hint= (4, 1),
                    )
        
        # dropdown
        dropdown = TopicDropdown(size_hint= (.5, 1))
        dropdown_topic_id = f"{DROPDOWN_TOPIC_ID_PREFIX}{self.topic_container_id_counter}"
        dropdown.bind(on_select= lambda instance, x: setattr(btn, 'text', x))
        grid.ids[dropdown_topic_id] = dropdown

        btn.bind(on_release=dropdown.open)
        btn.add_widget(dropdown)

        grid.ids[btn_select_topic_id] = btn
        grid.add_widget(btn)

        # bind update topics
        
        update_topic_callback_chain.append(dropdown.update)

        # label checkbox

        grid.add_widget(Label(text= "Value:"))

        # checkbox
        checkbox = CheckBox()
        checkbox_topic_id = f"{CHECKBOX_BOOL_VALUE_ID_PREFIX}{self.topic_container_id_counter}"
        grid.ids[checkbox_topic_id] = checkbox
        grid.add_widget(checkbox)

        # label checkbox pub continuos

        grid.add_widget(Label(text= "Pub continuos:"))

        # checkbox pub continuos
        checkbox_pub_continuous = CheckBox()
        checkbox_pub_continuous_id = f"{CHECKBOX_PUB_CONTINUOS_ID_PREFIX}{self.topic_container_id_counter}"
        grid.ids[checkbox_pub_continuous_id] = checkbox_pub_continuous
        grid.add_widget(checkbox_pub_continuous)

        # btn pub
        def pub_function(btn, btn_pub, checkbox, topic_container_id_counter):
            dropdown.pub(btn.text, checkbox.active, checkbox_pub_continuous.active, topic_container_id_counter)
            if btn_pub.text == "Pub" and checkbox_pub_continuous.active: 
                btn_pub.text = "Publishing"
            elif btn_pub.text == "Publishing" and checkbox_pub_continuous.active:
                btn_pub.text = "Pub"

        btn_pub = Button(text= "Pub")
        btn_pub.on_release= lambda : pub_function(btn, btn_pub, checkbox, self.topic_container_id_counter)
        grid.add_widget(btn_pub)
        # btn_select_topic_id = f"{BTN_SELECT_TOPIC_ID_PREFIX}{topic_container_id_counter}"
     
        # btn = Button(
        #              text= "Select topic",
        #              size_hint= (4, 1),
        #             )
        
        
        # dropdown = TopicDropdown(size_hint= (.5, 1))
        # dropdown_topic_id = f"{DROPDOWN_TOPIC_ID_PREFIX}{topic_container_id_counter}"
        # dropdown.add_widget(Button(text= "Update topics",
        #                     on_release= dropdown.update(btn)))
        # btn.add_widget(dropdown)
        # self.ids[dropdown_topic_id] = dropdown
        # self.ids[btn_select_topic_id] = btn
        # self.topic_container.add_widget(btn)

        self.topic_container.add_widget(grid)

        self.topic_container_id_counter = self.topic_container_id_counter + 1
        self.topic_grid_h = self.topic_grid_h + 60
        self.grid_top = self.grid_top - 1



class TopicContainer(GridLayout):
    
    pass

class TopicDropdown(DropDown):
    
    ros_manager = RosManager()
    topic_list = []

    def update(self):


        topics = self.ros_manager.get_topics()

        if topics != self.topic_list:

            self.clear_widgets()
            for t in topics:
                btn = Button(text = f"{t}", height=44, size_hint_y=None)
                btn.bind(on_release= lambda btn: self.select(btn.text))
                self.add_widget(btn)
            
        # self.bind(on_select= lambda instance, x: setattr(btn_select_item, 'text', x))

    def pub(self, topic, value, pub_continuous, publisher_id):

        print(f"topic: {topic}")
        print(f"value: {value}")
        print(f"publisher_id: {publisher_id}")
        self.ros_manager.pub_bool(topic, value, pub_continuous, publisher_id)


class ButtonSelectTopic(Widget):
    # dropdown = ObjectProperty(DropDown)
    def print(self, str):
        self.dropdown.create(self)
        self.dropdown.open()
        print(str)


# class TopicDropdown(Widget):

#     ros_manager = RosManager()


#     def create(self):

#         topics = self.ros_manager.get_topics()

#         dropdown = DropDown()
#         for t in topics:
#             btn = Button(text = f"{t}", height=44, size_hint_y=None)
#             btn.bind(on_release= lambda btn: dropdown.select(btn.text))
#             dropdown.add_widget(btn)

#         btn_select_item = Button(text='Select Item', size=(600, 44), pos=(100, 100))
#         btn_select_item.bind(on_release=dropdown.open)
#         dropdown.bind(on_select= lambda instance, x: setattr(btn_select_item, 'text', x))

#         return btn_select_item

class EverestApp(App):

    

    def build(self):
        # main_page.add_widget(Label(text = "Everest App", height=44, size_hint_y=None))
        
        # main_page.add_widget(ButtonTest())

        main_page = MainPage()
        # main_page.btn.bind(on_release=main_page.dropdown.open)
        # Clock.schedule_interval(main_page.dropdown.update, 100.0 / 60.0) 
        
        # ros_manager = RosManager()
        # topics = ros_manager.get_topics()

        # for t in topics:
        #     btn = Button(text = f"{t}", height=44, size_hint_y=None)
        #     btn.bind(on_release= lambda btn: self.topic_dropdown.select(btn.text))
        #     self.topic_dropdown.add_widget(btn)

        # btn_select_item = Button(text='Select Item', size=(600, 44), pos=(100, 100))
        # self.btn_select_topic.bind(self, on_release=self.topic_dropdown.open)
        # self.topic_dropdown.bind(on_select= lambda instance, x: setattr(self.btn_select_topic, 'text', x))

        # main_page.add_widget(btn_select_item)
        
        return main_page

if __name__ == '__main__':
    EverestApp().run()