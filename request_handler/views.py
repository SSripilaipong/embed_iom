import pytz
import datetime
import dateutil.parser
from django.http import QueryDict
from share_resource import control_data
from django.http import JsonResponse, HttpResponse
from .models import SensorData, SensorData2


def set_response_header(response):
    response.__setitem__("Content-type", "application/json")
    response.__setitem__("Access-Control-Allow-Origin", "*")
    return response


def get_status(request):
    if request.method != 'POST':
        return

    post = request.POST

    if 'last_timestamp' in post:
        last_timestamp = dateutil.parser.parse(post['last_timestamp'])
    else:
        last_timestamp = datetime.datetime.now() - datetime.timedelta(days=60)

    last_timestamp = datetime.datetime(last_timestamp.year, last_timestamp.month,
                                       last_timestamp.day, last_timestamp.hour,
                                       last_timestamp.minute, last_timestamp.second,
                                       )

    data = SensorData.objects.filter(timestamp__gt=last_timestamp,
                                     sensor_id=post['sensor_id'],
                                     sensor_type=post['sensor_type'],
                                     )

    response = []
    for record in data:
        obj = dict(timestamp=record.timestamp,
                   sensor_id=record.sensor_id,
                   sensor_type=record.sensor_type,
                   value=record.value,
                   )
        response.append(obj)

    response = sorted(response, key=lambda t: t['timestamp'])[-50:]
    response = JsonResponse(response, safe=False)
    return set_response_header(response)


def report_status(request):
    if request.method != 'POST':
        return

    post = request.POST

    timestamp = dateutil.parser.parse(post['timestamp'])
    timestamp = datetime.datetime(timestamp.year, timestamp.month,
                                  timestamp.day, timestamp.hour,
                                  timestamp.minute, timestamp.second,
                                  )
    query = dict(timestamp=timestamp,
                 sensor_id=post['sensor_id'],
                 sensor_type=post['sensor_type'],
                 )
    if SensorData.objects.filter(**query).exists():
        data = SensorData.objects.get(**query)
        data.value = post['value']
    else:
        data = SensorData(value=post['value'], **query)
    data.save()

    response = HttpResponse('')
    return set_response_header(response)


def get_status2(request):
    if request.method != 'POST':
        return

    post = request.POST

    if 'last_timestamp' in post:
        last_timestamp = dateutil.parser.parse(post['last_timestamp'])
    else:
        last_timestamp = datetime.datetime.now(tz=pytz.timezone('Asia/Bangkok'))
        last_timestamp -= datetime.timedelta(days=60)

    last_timestamp = datetime.datetime(last_timestamp.year, last_timestamp.month,
                                       last_timestamp.day, last_timestamp.hour,
                                       last_timestamp.minute, last_timestamp.second,
                                       )

    data = SensorData2.objects.filter(timestamp__gt=last_timestamp,
                                      sensor_id=post['sensor_id'],
                                      )

    response = []
    for record in data:
        obj = dict(timestamp=record.timestamp,
                   sensor_id=record.sensor_id,
                   light=record.light,
                   humid=record.humid,
                   )
        response.append(obj)

    response = sorted(response, key=lambda t: t['timestamp'])[-200:]
    response = JsonResponse(response, safe=False)
    return set_response_header(response)


def report_status2(request):
    if request.method != 'POST':
        return

    post = request.POST  # type: QueryDict
    if 'timestamp' in post:
        timestamp = dateutil.parser.parse(post['timestamp'])
    else:
        timestamp = datetime.datetime.now(tz=pytz.timezone('Asia/Bangkok'))
    timestamp = datetime.datetime(timestamp.year, timestamp.month,
                                  timestamp.day, timestamp.hour,
                                  timestamp.minute, timestamp.second,
                                  )
    query = dict(timestamp=timestamp,
                 sensor_id=post['sensor_id'],
                 )
    if SensorData2.objects.filter(**query).exists():
        data = SensorData2.objects.get(**query)
        data.light = post['light']
        data.humid = post['humid']
    else:
        data = SensorData2(light=post['light'], humid=post['humid'], **query)
    data.save()
    
    response = HttpResponse('')
    return set_response_header(response)


def control(request):
    if request.method != 'POST':
        return

    post = request.POST

    value = int(post['value'])

    assert post['sensor_type'] in ('light', 'water')
    if post['sensor_type'] == 'light':
        assert value in set(range(0, 5))
    elif post['sensor_type'] == 'water':
        assert value in (0, 1)
    control_data[post['sensor_id']][post['sensor_type']] = value

    response = HttpResponse('')
    return set_response_header(response)


def get_control(request):
    if request.method != 'POST':
        return

    post = request.POST

    response = JsonResponse(control_data[post['sensor_id']])
    return set_response_header(response)
