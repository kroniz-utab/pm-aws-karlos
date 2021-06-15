from django.core.mail.message import EmailMultiAlternatives
from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template
from datetime import datetime

def send_html_email(request):
    htmly = get_template('bee_template.html')

    subject = 'Mencoba mengirimkan email'
    msg = 'Coba aja dulu, dikembangin nanti'
    
    recipient_list = [
        'adehf12@gmail.com', 
        'adexxperient@gmail.com',
        # 'm1471710@bangkit.academy'
    ]
    today = datetime.today().strftime('%d-%m-%Y')
    context = {
        'date':today
    }
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject=subject, body=msg, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return HttpResponse('done')