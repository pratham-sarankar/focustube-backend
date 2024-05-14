from enum import Enum


class UploadDateFilter(str, Enum):
    lastHour = 'lastHour'
    today = 'today'
    thisWeek = 'thisWeek'
    thisMonth = 'thisMonth'
    thisYear = 'thisYear'
