from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    full_link_server = f'http://34.67.71.48/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте! Пожалуйста активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти этой по ссылке: \n{full_link}\n{full_link_server}',
        'forexempl@gmail.com',
        [user],
        fail_silently=False
    )


def send_reset_email(user):
    code = user.activation_code
    email = user.email
    send_mail('Письмо для сброса пароля!',
              f'Ваш код сброса пароля {code}', 'from@example.com',
              [email, ], fail_silently=False)


def send_notification(user_email, order_id, price):
    send_mail('Уведомления о создание нового заказа!',
              f''' Вы создали заказ №{order_id}, ожидайте звонка!
               Полная стоимость вашего заказа: {price}.
                Спасибо за то что выбрали нас!''',
              "from@example.com",
              [user_email, ],
              fail_silently=False
              )