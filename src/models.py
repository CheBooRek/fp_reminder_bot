import yaml
from typing import Optional
from pydantic import BaseModel


class JobSchedule(BaseModel):
    trigger: Optional[str] = 'cron'
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None


class BotInfo(BaseModel):
    name: str
    job_schedule: JobSchedule
    notification_message: Optional[str] = ''
    start_message: Optional[str] = ''


class Paths(BaseModel):
    log_path: str
    id_list_path: str


class Config(BaseModel):
    bot: BotInfo
    paths: Paths
