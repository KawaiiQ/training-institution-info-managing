from django.apps import AppConfig
from django.db.models.signals import post_migrate


def callback(sender, **kwargs):
    from .transactions import User as UserOperation
    from .models import User
    print('')
    print('#########################')
    print('#        kawaiiQ        #')
    print('#########################')
    print('')
    print('检查初始用户')
    if not User.objects.filter(username='korosensei').exists():
        print('用户不存在，创建用户 殺せんせー')
        UserOperation.create_admin('korosensei', 'big_boss', '殺せんせー', '12345678910')
        print('创建完成，请使用账号korosensei（密码为big_boss）登录系统')
    else:
        print('账户已经存在')


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        post_migrate.connect(callback, sender=self)
