# IoM

### requirements:
```
python 3.6.3
django 2.0.2
```


### runserver:
```
python manage.py runserver 0.0.0.0:<port>
```
choose a port that works for you. (typically 80, 8080)

example:
```
python manage.py runserver 0.0.0.0:8080
```


### monitoring and report simulation
files are
 * /monitor/monitor2.html
 * /monitor/reporter2.html

to test the monitor and reporter, find out your ip address and put it in URL field with your port.

for example, http://192.168.43.97:8080

if your home wifi doesn't work, maybe ports are blocked, try your mobile hotspot.
