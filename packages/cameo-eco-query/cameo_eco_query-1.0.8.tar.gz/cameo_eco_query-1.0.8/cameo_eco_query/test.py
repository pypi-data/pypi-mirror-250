from query_handler import get_event_gmap_info

if __name__ == '__main__':
    temp = get_event_gmap_info('上個月17號三峽發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)

    temp = get_event_gmap_info('5月12號台中市的北屯區東光路550之11號，有回收廠的大量廢棄物發生了火警')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)

    temp = get_event_gmap_info('三峽發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)

    temp = get_event_gmap_info('三峽昨天發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)


    temp = get_event_gmap_info('昨天下午三點三峽發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)


    temp = get_event_gmap_info('5月12號清晨六點左右，台中市的北屯區東光路550之11號，有回收廠的大量廢棄物發生了火警')
    try:
        print(temp['data'])
    except TypeError:

        print(temp)

    temp = get_event_gmap_info('現在三峽發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)

    temp = get_event_gmap_info('上個月17號下午三點三峽發生火災')
    try:
        print(temp['data'])
    except TypeError:
        print(temp)

    # error, error, error, error, success, success, success, success