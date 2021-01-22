# from django.apps import AppConfig
#
#
# class EcomadminpanelConfig(AppConfig):
#     name = 'ecomadminpanel'

from suit.apps import DjangoSuitConfig

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'