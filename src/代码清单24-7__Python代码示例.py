from agents import Agent
from agents.session import Session
from your_cloud_sync import CloudSync

class CloudSession(Session):
    """支持云同步的 Session"""

    def __init__(self, *args, sync: CloudSync, **kwargs):
        super().__init__(*args, **kwargs)
        self.sync = sync

    def on_message(self, message):
        # 发送消息到云端同步
        self.sync.push(message)

    def sync_from_cloud(self):
        # 从云端拉取同步
        messages = self.sync.pull()
        for msg in messages:
            self.add_message(msg)