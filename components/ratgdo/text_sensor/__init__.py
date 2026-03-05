import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

from .. import RATGDO_CLIENT_SCHMEA, ratgdo_ns, register_ratgdo_child

DEPENDENCIES = ["ratgdo"]

# Track which sensor types have been used
USED_TYPES: set[str] = set()

RATGDOTextSensor = ratgdo_ns.class_(
    "RATGDOTextSensor", text_sensor.TextSensor, cg.Component
)
RATGDOTextSensorType = ratgdo_ns.enum("RATGDOTextSensorType")

CONF_TYPE = "type"
TYPES = {
    "ttc_state": RATGDOTextSensorType.RATGDO_TTC_STATE,
}


def validate_unique_type(config):
    """Validate that each text sensor type is only used once."""
    sensor_type = config[CONF_TYPE]
    if sensor_type in USED_TYPES:
        raise cv.Invalid(f"Only one text sensor of type '{sensor_type}' is allowed")
    USED_TYPES.add(sensor_type)
    return config


CONFIG_SCHEMA = cv.All(
    text_sensor.text_sensor_schema(RATGDOTextSensor)
    .extend(
        {
            cv.Required(CONF_TYPE): cv.enum(TYPES, lower=True),
        }
    )
    .extend(RATGDO_CLIENT_SCHMEA),
    validate_unique_type,
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await text_sensor.register_text_sensor(var, config)
    await cg.register_component(var, config)
    cg.add(var.set_text_sensor_type(config[CONF_TYPE]))
    await register_ratgdo_child(var, config)
