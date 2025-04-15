from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
# 添加字體相關導入
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os
from models import TaskManager, Task

# 確保 data/icons 目錄存在
os.makedirs('data/icons', exist_ok=True)

# 添加字體設定 - 支援中文顯示
# 嘗試使用系統上常見的中文字體
fonts_to_try = [
    # Windows 中文字體
    "C:/Windows/Fonts/msjh.ttc",  # 微軟正黑體
    "C:/Windows/Fonts/simsun.ttc",  # 新宋體
    "C:/Windows/Fonts/msyh.ttc",  # 微軟雅黑
    # macOS 中文字體
    "/System/Library/Fonts/PingFang.ttc",  # 蘋方
    # 常見中文字體
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
]

# 尋找可用的中文字體
chinese_font = None
for font_path in fonts_to_try:
    if os.path.exists(font_path):
        chinese_font = font_path
        break

# 如果找到了中文字體，就註冊它
if chinese_font:
    LabelBase.register("DroidSansFallback", chinese_font)
else:
    print("警告：找不到中文字體，文字可能無法正常顯示")

class TaskItem(BoxLayout):
    """表示單個任務項目的佈局。"""
    id = StringProperty('')  # 任務的唯一識別碼
    description = StringProperty('')  # 任務描述
    completed = BooleanProperty(False)  # 任務完成狀態
    
    def toggle_completed(self, checkbox, value):
        """切換任務的完成狀態。"""
        app = App.get_running_app()
        app.task_manager.toggle_task_completed(self.id)
        # 更新界面
        app.root.update_task_lists()


class AddTaskDialog(ModalView):
    """添加新任務的對話框。"""
    
    def add_task(self):
        """添加新任務並關閉對話框。"""
        task_text = self.ids.task_input.text.strip()
        if task_text:
            app = App.get_running_app()
            app.task_manager.add_task(task_text)
            # 更新界面
            app.root.update_task_lists()
            # 清空輸入並關閉對話框
            self.ids.task_input.text = ""
            self.dismiss()


class MainScreen(Screen):
    """應用的主屏幕。"""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # 在屏幕初始化後更新任務列表
        Clock.schedule_once(self.update_task_lists, 0.1)
    
    def show_add_task_dialog(self):
        """顯示添加任務的對話框。"""
        dialog = AddTaskDialog()
        dialog.open()
    
    def update_task_lists(self, *args):
        """更新待完成和已完成任務列表。"""
        app = App.get_running_app()
        
        # 清空當前任務列表
        incomplete_container = self.ids.incomplete_tasks_container
        completed_container = self.ids.completed_tasks_container
        
        # 移除舊的任務項目（保留標題標籤）
        for container in [incomplete_container, completed_container]:
            for child in list(container.children)[:-1]:
                container.remove_widget(child)
        
        # 添加未完成任務
        for task in app.task_manager.get_incomplete_tasks():
            task_item = TaskItem()
            task_item.id = task.id
            task_item.description = task.description
            task_item.completed = task.completed
            incomplete_container.add_widget(task_item)
        
        # 添加已完成任務
        for task in app.task_manager.get_completed_tasks():
            task_item = TaskItem()
            task_item.id = task.id
            task_item.description = task.description
            task_item.completed = task.completed
            completed_container.add_widget(task_item)


class ToDoApp(App):
    """To-Do App 的主應用類。"""
    
    def build(self):
        """構建應用的主界面。"""
        # 設置任務管理器，存儲到數據文件夾
        self.task_manager = TaskManager(os.path.join('data', 'tasks.json'))
        
        # 如果文件不存在，添加一些示例任務
        if not self.task_manager.tasks:
            self.add_sample_tasks()
        
        # 加載 Kivy 佈局文件
        return MainScreen()
    
    def add_sample_tasks(self):
        """添加一些示例任務用於演示。"""
        self.task_manager.add_task("準備會議材料")
        self.task_manager.add_task("回覆重要郵件")
        self.task_manager.add_task("完成專案報告")
        self.task_manager.add_task("購買生日禮物")
        
        # 將一些任務標記為已完成
        tasks = self.task_manager.tasks
        if len(tasks) >= 2:
            self.task_manager.toggle_task_completed(tasks[-1].id)
            self.task_manager.toggle_task_completed(tasks[-2].id)