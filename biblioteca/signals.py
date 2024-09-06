from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from biblioteca.models import Emprestimo, Livro

@receiver(post_delete, sender=Emprestimo)
def emprestimo_pos_delete(sender, instance, **kwargs):
    print('teste')