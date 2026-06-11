from .models import Streak
from django.utils import timezone

def get_streak(id):
    return Streak.objects.get(user_streak_id=id)


def create_streak(id):
    Streak.objects.create(user_streak_id=id)

def top_employee_on_streak(id):
    return Streak.objects.select_related('user_streak').filter(user_streak__organization_id=id).order_by('-count').first().user_streak.user_name

def streak_logic(id):
    streak=get_streak(id)
    time_now=timezone.now().date()
    if streak.last_activity_date is None:
        streak.last_activity_date=time_now
        streak.count=1
        if streak.max_streak<streak.count:
            streak.max_streak=streak.count
        streak.save()
    else:
        last_acitivity=streak.last_activity_date.date()
        differnce=time_now-last_acitivity
        if differnce.days==0:
            pass
        elif differnce.days==1:
            streak.last_activity_date=time_now
            streak.count+=1
            if streak.max_streak<streak.count:
                streak.max_streak=streak.count
            streak.save()
        else:
            streak.last_activity_date=time_now
            streak.count=0
            streak.save()