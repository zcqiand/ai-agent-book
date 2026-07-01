from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import asyncio

class EventType(str, Enum):
    """事件类型"""
    ORDER_CREATED = "order.created"
    ORDER_PAID = "order.paid"
    ORDER_SHIPPED = "order.shipped"
    INVENTORY_LOW = "inventory.low"
    MONITORING_ALERT = "monitoring.alert"

@dataclass
class WorkflowEvent:
    """工作流事件"""
    event_id: str
    event_type: EventType
    payload: dict
    timestamp: str
    source: str

class EventDrivenWorkflow:
    """事件驱动工作流引擎"""

    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = {}
        self.workflow_registry: Dict[str, callable] = {}

    def register_event_handler(
        self,
        event_type: EventType,
        handler: Callable
    ):
        """注册事件处理器"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def register_workflow(
        self,
        workflow_id: str,
        workflow: Callable
    ):
        """注册工作流"""
        self.workflow_registry[workflow_id] = workflow

    async def handle_event(self, event: WorkflowEvent):
        """处理事件"""
        print(f"收到事件: {event.event_type} from {event.source}")

        # 查找对应的处理器
        handlers = self.handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                # 创建工作流实例
                workflow_id = handler(event)
                if workflow_id and workflow_id in self.workflow_registry:
                    workflow = self.workflow_registry[workflow_id]
                    await workflow.run(event.payload)
            except Exception as e:
                print(f"处理事件失败: {str(e)}")


# 使用示例
async def order_created_workflow(payload: dict):
    """订单创建工作流"""
    print(f"处理新订单: {payload.get('order_id')}")

    # 1. 验证订单
    order = payload
    # 2. 检查库存
    # 3. 等待支付
    # 4. 触发后续流程

    return "订单处理完成"
