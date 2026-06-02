from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class LearningGoal:
    """学习目标"""
    goal_id: str
    title: str
    description: str
    status: str  # pending, in_progress, completed
    target_date: str
    completed_at: str = None

@dataclass
class ChapterReview:
    """章节复习记录"""
    chapter_id: str
    review_date: str
    understanding_level: int  # 1-5
    notes: str
    practice_status: str  # not_done, partial, completed

class LearningTracker:
    """个人学习追踪系统"""

    def __init__(self):
        self.goals: List[LearningGoal] = []
        self.chapter_reviews: Dict[str, ChapterReview] = {}

    def add_goal(self, goal: LearningGoal):
        """添加学习目标"""
        self.goals.append(goal)

    def review_chapter(self, chapter_id: str, review: ChapterReview):
        """记录章节复习"""
        self.chapter_reviews[chapter_id] = review

    def get_learning_summary(self) -> dict:
        """获取学习总结"""
        completed_goals = [g for g in self.goals if g.status == "completed"]
        in_progress_goals = [g for g in self.goals if g.status == "in_progress"]

        avg_understanding = 0
        if self.chapter_reviews:
            avg_understanding = sum(
                r.understanding_level for r in self.chapter_reviews.values()
            ) / len(self.chapter_reviews)

        return {
            "total_goals": len(self.goals),
            "completed": len(completed_goals),
            "in_progress": len(in_progress_goals),
            "chapters_reviewed": len(self.chapter_reviews),
            "avg_understanding": round(avg_understanding, 1)
        }


# 使用示例
tracker = LearningTracker()

# 添加学习目标
tracker.add_goal(LearningGoal(
    goal_id="g_001",
    title="掌握LangGraph",
    description="深入学习LangGraph状态管理和复杂工作流",
    status="in_progress",
    target_date="2026-06-01"
))

# 记录章节复习
tracker.review_chapter("ch_011", ChapterReview(
    chapter_id="ch_011",
    review_date="2026-05-09",
    understanding_level=4,
    notes="StateGraph是核心概念，需要多实践",
    practice_status="partial"
))

# 获取总结
summary = tracker.get_learning_summary()
print(f"学习进度：{summary['completed']}/{summary['total_goals']} 已完成")
print(f"章节复习：{summary['chapters_reviewed']} 章，平均理解度 {summary['avg_understanding']}/5")