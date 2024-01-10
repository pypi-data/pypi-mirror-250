from django.dispatch import receiver

from zs_utils.support import models, signals, constants, services


@receiver(signal=signals.support_ticket_status_changed)
def create_system_message(ticket: models.AbstractSupportTicket, prev_status: constants.SUPPORT_TICKET_STATUSES, **kwargs):
    services.CommonSupportTicketService.create_system_message_after_status_change(
        ticket=ticket,
        prev_status=prev_status,
    )
