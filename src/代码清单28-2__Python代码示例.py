class OrderManager:
    """订单管理器"""

    def __init__(self):
        self.orders = {}

    def create_order(self, user_id: str, items: list) -> dict:
        """创建订单"""
        order_id = f"ORD_{len(self.orders) + 1:04d}"

        order = {
            "order_id": order_id,
            "user_id": user_id,
            "items": items,
            "status": "pending",
            "total": sum(item["price"] for item in items)
        }

        self.orders[order_id] = order
        return order

    def confirm_order(self, order_id: str) -> dict:
        """确认订单"""
        if order_id in self.orders:
            self.orders[order_id]["status"] = "confirmed"
            return {"success": True, "order": self.orders[order_id]}
        return {"success": False, "error": "订单不存在"}

    def cancel_order(self, order_id: str) -> dict:
        """取消订单"""
        if order_id in self.orders:
            order = self.orders[order_id]
            if order["status"] in ["pending", "confirmed"]:
                order["status"] = "cancelled"
                return {"success": True}
        return {"success": False, "error": "无法取消"}

order_manager = OrderManager()