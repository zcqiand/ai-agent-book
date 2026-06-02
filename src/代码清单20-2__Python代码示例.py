# 工具定义示例
def get_weather(location: str) -> str:
    """获取指定城市的天气信息

    参数:
        location: 城市名称，中文或英文，如"北京"、"Tokyo"

    返回:
        天气信息字符串，包括温度、天气状况等
    """
    # 实际实现会调用天气 API
    return f"{location}今天晴，温度15-25度"