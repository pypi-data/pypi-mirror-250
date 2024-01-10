from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from zs_utils.support import services
from zs_utils.views import CustomModelViewSet


__all__ = [
    "BaseSupportTicketView",
    "BaseSupportTicketMessageView",
    "BaseSupportTicketMessageFileView",
]


class BaseSupportTicketView(CustomModelViewSet):
    """
    Абстрактный View для создания и просмотра тикетов (SupportTicket)
    """
    not_allowed_actions = [
        "destroy",
        "update",
        "partial_update",
    ]

    @classmethod
    def get_support_ticket_service_model(cls):
        raise NotImplementedError("В сервисе должен быть определён метод получения модели SupportTicketService")

    @classmethod
    def get_create_support_ticket_serializer_model(cls):
        raise NotImplementedError(
            "В сервисе должен быть определён метод получения модели CreateSupportTicketSerializer"
        )

    def get_queryset_filter_kwargs(self) -> dict:
        user = self.get_user()
        if user.is_staff:
            return {}
        else:
            return {"user": user}

    @action(detail=True, methods=["POST"])
    def close(self, request, *args, **kwargs):
        """
        Закрытие тикета
        """
        services.CommonSupportTicketService.close_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def reopen(self, request, *args, **kwargs):
        """
        Открыть закрытый тикет
        """
        services.CommonSupportTicketService.reopen_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def set_viewed(self, request, *args, **kwargs):
        services.CommonSupportTicketService.set_ticket_viewed(user=self.get_user(), ticket=self.get_object())
        return self.build_response()


class BaseSupportTicketMessageView(CustomModelViewSet):
    """
    Абстрактный View для создания/удаления/обновления/просмотра сообщений тикета (SupportTicketMessage)
    """
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]


class BaseSupportTicketMessageFileView(CustomModelViewSet):
    """
    Абстрактный View для создания/удаления/обновления/просмотра файлов сообщений (SupportTicketMessageFile)
    """
    parser_classes = (MultiPartParser,)
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]
