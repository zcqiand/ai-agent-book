from agents import Agent
from agents.session import Session

class OrderingSession(Session):
    """订餐会话"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart = []
        self.current_restaurant = None

    def add_to_cart(self, item: dict):
        """添加商品到购物车"""
        self.cart.append(item)

    def get_cart_total(self) -> float:
        """计算购物车总价"""
        return sum(item["price"] for item in self.cart)

    def clear_cart(self):
        """清空购物车"""
        self.cart = []

# 使用
session = OrderingSession(
    agent=main_agent,
    session_id="user_ordering_123"
)

session.add_to_cart({"name": "宫保鸡丁", "price": 38})
session.add_to_cart({"name": "米饭", "price": 3})

print(f"购物车总价: {session.get_cart_total()}")  # 41