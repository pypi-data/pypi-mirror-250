import psutil
from typing import Sequence


def check_env(appendix_packages: Sequence[str]) -> dict:
    result = {
        'package': {}
    }

    for package in appendix_packages:
        try:
            eval(f'exec("import {package}")')
            result['package'][package] = eval(f'{package}.__version__')
        except:
            result['package'][package] = False

    try:
        import torch
        result['gpu'] = torch.cuda.is_available()
    except:
        result['gpu'] = False

    try:
        from nvitop import Device
        devices = Device.all()

        result['gpu_count'] = len(devices)
        result['gpu_info'] = []

        for device in devices:
            result['gpu_info'].append({
                'name': device.name(),
                'total_memory': device.memory_total() / 1024 / 1024,
                'available_memory': device.memory_used() / 1024 / 1024,
                'fan_speed': device.fan_speed(),
                'temperature': device.temperature()
            })

    except:
        pass

    result['total_memory'] = psutil.virtual_memory().total / 1024 / 1024
    result['available_memory'] = psutil.virtual_memory().available / 1024 / 1024
    result['available_disk'] = psutil.disk_usage('./').free / 1024 / 1024

    return result


def cache_nltk() -> None:
    '''
    将NLTK的文件缓存到本地
    '''
    pass
