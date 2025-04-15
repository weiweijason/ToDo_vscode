"""
To-Do App 應用入口點
"""
import os
from kivy.resources import resource_add_path
from todo_app import ToDoApp

if __name__ == '__main__':
    # 添加資源路徑
    resource_add_path(os.path.abspath(os.path.dirname(__file__)))
    
    # 創建並運行應用
    app = ToDoApp()
    app.run()