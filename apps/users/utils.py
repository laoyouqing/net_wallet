import json
from urllib.parse import urlencode

import requests

from users.models import UserToken, User



def has_exist(token):
    params = {
        'token': token,
        'api': 'user_info',
    }
    str_param = urlencode(params)
    resp = requests.post('http://wangbo.ie1e.com/ifs/interface.ashx', data=str_param,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
    resp = json.loads(resp.content)
    print(resp)
    if resp['resultcode'] == '0':
        id = resp['data']['user']['id']
        # user_token = UserToken.objects.filter(token=token, user_id=id)
        # if not user_token:
        #     UserToken.objects.create(token=token, user_id=id)
        try:
            user = User.objects.get(id=id)
            wbc_balance = resp['data']['user']['point']
            user.wbc_balance=wbc_balance
            user.save()
        except:
            name=resp['data']['user']['name']
            if name=='':
                name = resp['data']['user']['nickname']
            username = name
            photo = resp['data']['user']['headimg']
            email = resp['data']['user']['email']
            fri_code = resp['data']['user']['FrinQCode']
            pay_code = resp['data']['user']['PayQCode']
            wbc_balance = resp['data']['user']['point']
            telphone = resp['data']['user']['phone']
            user = User.objects.create(id=id, username=username, photo=photo, email=email, fri_code=fri_code,
                                       pay_code=pay_code, wbc_balance=wbc_balance,telphone=telphone)

        return user
    else:
        return None



def check_year(year):
    if (year%4==0 and year%100!=0) or year%400==0:
        li=[31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        li=[31,28,31,30,31,30,31,31,30,31,30,31]
    return li



def payapi(from_paycode,to_paycode,point):
    params = {
        'fromPayCode': from_paycode,
        'toPayCode': to_paycode,
        'point': point,
        'api': 'transfer',
    }
    str_param = urlencode(params)
    resp = requests.post('http://wangbo.ie1e.com/ifs/interface.ashx', data=str_param,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
    resp=json.loads(resp.content.decode())
    return resp