from typing import List

def calculate_word_overlap(response: str, reference: str) -> float:
    """计算与参考答案的词汇重叠度"""
    response_words = set(response)
    reference_words = set(reference)

    if not reference_words:
        return 0.0

    overlap = response_words & reference_words
    return len(overlap) / len(reference_words)

def calculate_length_ratio(response: str, reference: str) -> float:
    """计算回答长度与参考答案的比例"""
    if not reference:
        return 1.0
    return len(response) / len(reference)

def calculate_fluency_score(text: str) -> float:
    """简单的流畅性评估（基于句子完整性）"""
    sentences = text.replace("!", ".").replace("?", ".").split(".")
    complete = sum(1 for s in sentences if len(s.strip()) > 10)
    return complete / max(len(sentences), 1)

# 使用
response = "大语言模型是一种使用深度学习技术训练的自然语言处理模型，能够理解和生成文本。"
reference = "大语言模型是基于深度学习技术的语言模型，能处理自然语言任务。"

print(f"词汇重叠度: {calculate_word_overlap(response, reference):.2f}")
print(f"长度比例: {calculate_length_ratio(response, reference):.2f}")
print(f"流畅性评分: {calculate_fluency_score(response):.2f}")
