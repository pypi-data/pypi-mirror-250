# Local Vol model using Monte Carlo method
# TODO rev: This is an advanced model. Relocate to a new folder.


from qablet.base.base import Model, ModelStateBase
from .. import _qablet


# Define the Model Class
class LVMCModel(Model):
    __PARAM_SCHEMA_NAME__ = "LV"

    def state_class(self):
        return ModelStateBase

    def price_method(self):
        return _qablet.mc_lv_price
