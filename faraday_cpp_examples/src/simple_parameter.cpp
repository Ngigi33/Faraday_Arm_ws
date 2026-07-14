#include <rclcpp/rclcpp.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>
#include <string>
#include <vector>

class SimpleParmeter : public rclcpp::Node
{
public:
    SimpleParmeter() : Node("simple_parameter")
    {
        declare_parameter<int>("simple_int_param",28);
        declare_parameter<std::string>("simple_string_param","ngigi");

        param_callback_handle_=add_on_set_parameters_callback(std::bind(&SimpleParmeter::paramChangeCallback, this, _1));
    }


private:
    OnSetParameterCallbackHandle::SharedPtr param_callback_handle_;

    rcl_interfaces::msg::SetParametersResult paramChangeCallback(const std::vector<rclcpp::Parameter>&parameters)
    {
        rcl_interfaces::msg::SetParametersResult result;
        for (const auto& param : parameters)
        {
           if (param.get_name() == "simple_int_param" && param.get_type() == rclcpp:ParameterType::PARAMETER_INTEGER)
           {
            RCLCPP_INFO_STREAM(get_logger(),"Param simple_int_param changed !!!! New VALUE = "<<param.as_int());
            result.succesful =True
           }
            if (param.get_name() == "simple_string_param" && param.get_type() == rclcpp:ParameterType::PARAMETER_STRING)
           {
            RCLCPP_INFO_STREAM(get_logger(),"Param simple_string_param changed !!!! New VALUE = "<<param.as_string());
            result.succesful =True
           }
           
        }
        

    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimpleParmeter>());
    rclcpp::shutdown();
    return 0;
}
