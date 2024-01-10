from model_utils import Choices

from django.conf import settings
from django.utils.translation import gettext_lazy as _


SUPPORT_TICKET_QUESTION_TYPES = getattr(settings, 'SUPPORT_TICKET_QUESTION_TYPES')

SUPPORT_TICKET_STATUSES = Choices(
    ("PENDING", _("Ожидает рассмотрения")),
    ("OPEN", _("Открыто")),
    ("CLOSED_BY_USER", _("Закрыто пользователем")),
    ("CLOSED_BY_MANAGER", _("Закрыто менеджером")),
    ("CLOSED_AUTO", _("Закрыто из-за отсутствия активности")),
)

SUPPORT_TICKET_ACTIVE_STATUSES = SUPPORT_TICKET_STATUSES.subset("PENDING", "OPEN")

SUPPORT_TICKET_ACTIVE_STATUSES_LIST = [item[0] for item in SUPPORT_TICKET_ACTIVE_STATUSES]

SUPPORT_TICKET_CLIENT_STATUSES = Choices(
    ("PENDING", _("В работе")),
    ("RESPONDED", _("Получен ответ")),
    ("CLOSED", _("Закрыто")),
)

MAX_OPEN_TICKET = getattr(settings, 'MAX_OPEN_TICKET', 10)
