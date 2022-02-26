from django.core.mail import send_mail


def send(user_email):
    send_mail(
        "Test",
        "HELLO! Did you get my message?",
        "fortestmysite@gmail.com",
        [user_email],
        fail_silently=False
    )
