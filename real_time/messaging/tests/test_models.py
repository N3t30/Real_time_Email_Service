from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message

User = get_user_model()

class MessageModelTest(TestCase):

    def setUp(self):
        # Criando usuários com e-mails exclusivos para evitar conflitos
        self.sender = get_user_model().objects.create_user(
            username='sender', 
            email='sender@example.com',
            password='password123'
        )
        self.receiver = get_user_model().objects.create_user(
            username='receiver', 
            email='receiver@example.com', 
            password='password123'
        )
        
        # Criando a mensagem para os testes
        self.message = Message.objects.create(
            sender=self.sender, 
            receiver=self.receiver, 
            content="Hello, how are you?"
        )

    def test_message_creation(self):
        """Testa se a mensagem foi criada corretamente"""
        # Verificando se o remetente e o destinatário são os esperados
        self.assertEqual(self.message.sender.username, 'sender')
        self.assertEqual(self.message.receiver.username, 'receiver')
        # Verificando se o conteúdo da mensagem está correto
        self.assertEqual(self.message.content, "Hello, how are you?")
        # Verificando se o timestamp foi preenchido corretamente
        self.assertIsNotNone(self.message.timestamp)

    def test_message_str(self):
        """Testa a representação em string do modelo Message"""
        # Verificando se a string da mensagem segue o formato esperado
        self.assertEqual(str(self.message), f'Message from sender to receiver at {self.message.timestamp}')

    def test_sent_messages(self):
        """Testa a relação de mensagens enviadas"""
        # Verificando se a mensagem aparece nas mensagens enviadas pelo remetente
        self.assertIn(self.message, self.sender.sent_messages.all())

    def test_received_messages(self):
        """Testa a relação de mensagens recebidas"""
        # Verificando se a mensagem aparece nas mensagens recebidas pelo destinatário
        self.assertIn(self.message, self.receiver.received_messages.all())
    
    def test_message_count(self):
        """Testa se o número de mensagens enviadas e recebidas está correto"""
        # Verificando se o número de mensagens enviadas pelo remetente é 1
        self.assertEqual(self.sender.sent_messages.count(), 1)
        # Verificando se o número de mensagens recebidas pelo destinatário é 1
        self.assertEqual(self.receiver.received_messages.count(), 1)
