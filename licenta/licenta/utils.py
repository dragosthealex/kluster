import json


def validate_args(args):
    if None in args:
        print('See help')
        return False
    return True


def _json_success(message):
    return json.dumps({'status': 'SUCCESS', 'message': message})


def _json_error(e):
    return json.dumps({'status': 'ERROR', 'message': e})
