#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest, json, requests, time

def restget(url,token):
    urlprefix='http://127.0.0.1:5000/api/v1/'
    headers = {'Content-type': 'application/json','Authorization': 'JWT {0}'.format(token)}
    r = requests.get((urlprefix+url), headers=headers)
    return r.status_code,r.json()

def restpost(url,token,data):
    urlprefix='http://127.0.0.1:5000/api/v1/'
    headers = {'Content-type': 'application/json','Authorization': 'JWT {0}'.format(token)}
    r = requests.post((urlprefix+url), headers=headers,data=json.dumps(data))
    return r.status_code,r.json()

def restpatch(url,token,data):
    urlprefix='http://127.0.0.1:5000/api/v1/'
    headers = {'Content-type': 'application/json','Authorization': 'JWT {0}'.format(token)}
    r = requests.patch((urlprefix+url), headers=headers, data=json.dumps(data))
    return r.status_code,r.json()

def restdelete(url,token):
    urlprefix='http://127.0.0.1:5000/api/v1/'
    headers = {'Content-type': 'application/json','Authorization': 'JWT {0}'.format(token)}
    r = requests.delete((urlprefix+url), headers=headers)
    return r.status_code,r.json()

@pytest.fixture(scope="module")
def loginadmin(request):
    data = {"username":"root","password":"root"}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    url='http://127.0.0.1:5000/auth'
    response = requests.post(url, data=data_json, headers=headers)
    def fin():
        print('end')
    request.addfinalizer(fin)
    return response.json()

def test_users(loginadmin):
    token=loginadmin['access_token']
    assert len(token)==168
    assert restget('users/current',token) == (200,{'id': 1, 'login': 'root', 'passwordhash': '63a9f0ea7bb98050796b649e85481845', 'role': 'admin'})
    assert len(restget('users',token)[1]['users'])==1
    assert restget('users/4',token)==(404,{'error':'User not found'})
    assert restpost('users',token,data={'login':'alice','password':'alicepassword'})==(201,{'id': 2, 'login': 'alice', 'password': 'alicepassword'})
    assert restpost('users',token,data={'password':'bobpassword'})==(400,{'error':'Login must be provided'})
    test = restpost('users',token,data={'login':'bob'})
    assert test[1]['id']==3
    assert test[1]['login']=='bob'
    assert len(test[1]['password'])==8
    assert test[0]==201
    assert restpost('users',token,data={'login':'charlie'})[0]==201
    assert restpost('users',token,data={'login':'bob'})==(400,{'error':'Login must be unique'})
    assert len(restget('users',token)[1]['users'])==4
    assert restdelete('users/3',token)[0]==204
    assert restdelete('users/3',token)==(404,{'error':'User not found'})
    assert len(restget('users',token)['users'])==3
    assert restget('users/2',token)['login']=='alice'
    assert restpatch('users/2',token,data={'login':'alyx'})==201
    assert restget('users/2',token)['login']=='alyx'
    assert restdelete('users/5',token,data={'login':'charlie'})==(404,{'error':'user not found'})

if __name__ == '__main__':
    pytest.main('test_users.py')