import time
import subprocess
from playsound import playsound

subprocess.run(['speech-dispatcher'], shell=True, capture_output=True)


def notify(message, flag=None):
    if flag == 'charging':
        playsound('../charged.mp3')
    elif flag == 'discharging':
        playsound('../under_charged.mp3')

    subprocess.call(['spd-say', message])


while True:
    proc = subprocess.Popen('acpi', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        battery_status, error = proc.communicate()
    except:
        pass

    index_percent = str(battery_status).index('%')
    battery_percent = int(battery_status[index_percent - 3:index_percent])

    if 'Discharging' in battery_status:
        if battery_percent < 40:
            notify('Warning: Battery level is %s percent ,and discharging' % battery_percent, 'discharging')
    elif 'charging' in battery_status.casefold() and battery_percent > 80:
        notify('Warning: Battery level is %s percent ,and charging' % battery_percent, 'charging')

    time.sleep(10)
