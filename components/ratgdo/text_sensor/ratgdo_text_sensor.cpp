#include "ratgdo_text_sensor.h"
#include "../ratgdo_state.h"
#include "esphome/core/log.h"

namespace esphome {
namespace ratgdo {

    static const char* const TAG = "ratgdo.text_sensor";

    void RATGDOTextSensor::setup()
    {
        switch (this->type_) {
        case RATGDOTextSensorType::RATGDO_TTC_STATE:
            this->parent_->subscribe_ttc_state([this](TTCState state) {
                this->publish_state(TTCState_to_string(state));
            });
            // Publish current value in case sync already resolved before setup()
            this->publish_state(TTCState_to_string(*this->parent_->ttc_state));
            break;
        default:
            break;
        }
    }

    void RATGDOTextSensor::dump_config()
    {
        LOG_TEXT_SENSOR("", "RATGDO TextSensor", this);
        switch (this->type_) {
        case RATGDOTextSensorType::RATGDO_TTC_STATE:
            ESP_LOGCONFIG(TAG, "  Type: TTC State");
            break;
        default:
            break;
        }
    }

} // namespace ratgdo
} // namespace esphome
