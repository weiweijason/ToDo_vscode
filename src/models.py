from typing import Optional, List, Dict, Any
import json
import os
from datetime import datetime
import uuid

class Task:
    """表示一個待辦事項任務的類。"""
    
    def __init__(self, description: str, id: Optional[str] = None, completed: bool = False):
        """
        初始化一個新的 Task 實例。
        
        Args:
            description: 任務描述
            id: 任務唯一識別碼，如果未提供則自動生成
            completed: 任務是否已完成
        """
        self.id = id if id else str(uuid.uuid4())
        self.description = description
        self.completed = completed
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """將任務轉換為字典格式，方便 JSON 序列化。"""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """從字典創建任務實例。"""
        task = cls(
            description=data['description'],
            id=data['id'],
            completed=data['completed']
        )
        task.created_at = data.get('created_at', datetime.now().isoformat())
        return task
    
    def toggle_completed(self) -> None:
        """切換任務的完成狀態。"""
        self.completed = not self.completed


class TaskManager:
    """管理任務集合的類。"""
    
    def __init__(self, storage_file: str = 'tasks.json'):
        """
        初始化 TaskManager 實例。
        
        Args:
            storage_file: 存儲任務的 JSON 文件路徑
        """
        self.tasks: List[Task] = []
        self.storage_file = storage_file
        self.load_tasks()
    
    def add_task(self, description: str) -> Task:
        """
        添加新任務到任務列表。
        
        Args:
            description: 任務描述
            
        Returns:
            新創建的任務實例
        """
        task = Task(description=description)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        通過 ID 獲取任務。
        
        Args:
            task_id: 任務的唯一識別碼
            
        Returns:
            找到的任務，如果未找到則返回 None
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def toggle_task_completed(self, task_id: str) -> bool:
        """
        切換任務的完成狀態。
        
        Args:
            task_id: 任務的唯一識別碼
            
        Returns:
            如果找到並更新了任務則返回 True，否則返回 False
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.toggle_completed()
            self.save_tasks()
            return True
        return False
    
    def get_incomplete_tasks(self) -> List[Task]:
        """獲取所有未完成的任務。"""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """獲取所有已完成的任務。"""
        return [task for task in self.tasks if task.completed]
    
    def save_tasks(self) -> None:
        """將任務保存到 JSON 文件。"""
        tasks_data = [task.to_dict() for task in self.tasks]
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(os.path.abspath(self.storage_file)), exist_ok=True)
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)
    
    def load_tasks(self) -> None:
        """從 JSON 文件加載任務。"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"加載任務時出錯: {e}")
            self.tasks = []