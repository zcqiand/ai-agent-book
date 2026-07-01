import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
import croniter

class CronWorkflow:
    """定时工作流"""

    def __init__(self):
        self.jobs: Dict[str, dict] = {}

    def add_cron_job(
        self,
        job_id: str,
        cron_expression: str,
        handler: callable,
        enabled: bool = True
    ):
        """添加定时任务"""
        self.jobs[job_id] = {
            "cron": cron_expression,
            "handler": handler,
            "enabled": enabled,
            "last_run": None,
            "next_run": None
        }

    def get_next_run(self, job_id: str) -> datetime:
        """计算下次执行时间"""
        job = self.jobs.get(job_id)
        if not job:
            return None

        cron = croniter.croniter(job["cron"], datetime.now())
        return cron.get_next(datetime)

    async def run_scheduler(self):
        """运行调度器"""
        while True:
            now = datetime.now()

            for job_id, job in self.jobs.items():
                if not job["enabled"]:
                    continue

                next_run = self.get_next_run(job_id)
                job["next_run"] = next_run

                # 检查是否应该执行
                if next_run and now >= next_run:
                    try:
                        print(f"执行定时任务: {job_id}")
                        await job["handler"]()
                        job["last_run"] = now
                    except Exception as e:
                        print(f"定时任务执行失败: {job_id}, {str(e)}")

            await asyncio.sleep(60)  # 每分钟检查一次


# 使用示例
async def daily_report_workflow():
    """每日报告生成工作流"""
    print("生成每日报告...")

    # 1. 收集数据
    # 2. 生成报告
    # 3. 发送邮件

    print("每日报告生成完成")

# 添加定时任务
scheduler = CronWorkflow()
scheduler.add_cron_job(
    job_id="daily_report",
    cron_expression="0 8 * * *",  # 每天早上8点
    handler=daily_report_workflow
)
