import datetime
import time

def _get_hours_minutes_seconds(time_data):
    minutes, seconds = divmod(time_data.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds
            

def _format_time(time_list):
    result = ""
    hours, minutes, seconds = time_list
    if hours != 0:
        result += f"{hours}時間"
    if minutes != 0:
        result += f"{minutes}分"
    if seconds != 0:
        result += f"{seconds}秒"
    return result
    
class Timer:
    def __init__(self, user):
        self.user = user
        self._start_at = time.perf_counter()
        self._end_at = None
        self.is_new = True

    def stop(self):
        self._end_at = time.perf_counter()
        self.is_new = False
        delta = self._end_at - self._start_at
        return self._display_result(delta)

    def _display_result(self, delta):
        delta_time_data = datetime.timedelta(seconds=delta)
        hms = _get_hours_minutes_seconds(delta_time_data)
        return _format_time(hms)


class TimerList:
    _users = {}

    @classmethod
    def append(cls, user):
        cls._users[user] = Timer(user)
    
    @classmethod
    def is_new(cls, user):
        return user not in cls._users

    @classmethod
    def pop(cls, key):
        return cls._users.pop(key)