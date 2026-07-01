class CouponSystem:
    """优惠码系统"""

    COUPONS = {
        "FIRST10": {"discount": 0.1, "desc": "首单9折"},
        "SAVE20": {"discount": 20, "desc": "满100减20"},
    }

    def apply_coupon(self, coupon_code: str, amount: float) -> tuple[float, str]:
        """应用优惠码"""
        if coupon_code in self.COUPONS:
            coupon = self.COUPONS[coupon_code]
            if "discount" in coupon:
                discount = coupon["discount"]
                if discount < 1:  # 百分比折扣
                    return amount * (1 - discount), coupon["desc"]
                else:  # 固定金额折扣
                    return max(0, amount - discount), coupon["desc"]

        return amount, "优惠码无效"

coupon_system = CouponSystem()

# 测试
original = 150
final, desc = coupon_system.apply_coupon("SAVE20", original)
print(f"原价: {original}, 优惠后: {final}, 描述: {desc}")
# 原价: 150, 优惠后: 130, 描述: 满100减20
