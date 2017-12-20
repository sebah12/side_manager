from .models import Marca, Item, Remito, CampoRemito, ItemLogs
import datetime


def get_stats(item_id):
    """
    Get statistics of entradas y salidas for the las month
    for item_id
    """
    span = 35                   # span en dias
    logs_retirados = get_logs(item_id, False, span)
    retirados = (get_split_cant(logs_retirados))
    total = 0
    for entry in retirados:
        total += entry
    retirados.append(total)
    logs_ingresados = get_logs(item_id, True, span)
    ingresados = (get_split_cant(logs_ingresados))
    total = 0
    for entry in ingresados:
        total += entry
    ingresados.append(total)
    stats = []
    stats.append(retirados)
    stats.append(ingresados)
    return stats


def get_logs(item_id, action, span):
    """
    Get logs corresponding to item_id and action (1 ingreso, 0 egreso)
    starting from current date dating to current date - span (days)
    """
    logs = ItemLogs.objects.all().filter(item_id=item_id, action=action)
    # if logs:
    date = datetime.datetime.now().date()
    DD = datetime.timedelta(days=span)
    logs = logs.filter(created_at__gte=date-DD)
    return logs


def add_cant_logs(logs):
    """
    Return the sum of all log cuantities
    """
    result = 0
    for log in logs:
        result += log.cantidad
    return result


def get_split_cant(logs):
    """
    Return the cuantities of separate weeks in a list
    """
    date = datetime.datetime.now().date()
    span = date.weekday() - 1
    DD = datetime.timedelta(days=span)
    result = []
    # if logs:
    logs_n = logs.filter(created_at__gte=(date-DD))
    result.append(add_cant_logs(logs_n))
    span = 7
    for x in range(0, 3):
        date = date-DD
        DD = datetime.timedelta(days=span)
        logs_n = logs.filter(created_at__gte=(date-DD),
                             created_at__lt=date)
        result.append(add_cant_logs(logs_n))
    return result
