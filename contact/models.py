from django.db import models


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('order', 'Вопрос о заказе'),
        ('product', 'Вопрос о товаре'),
        ('collaboration', 'Сотрудничество'),
        ('other', 'Другое'),
    ]

    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Тема', max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.name} — {self.get_subject_display()}'
