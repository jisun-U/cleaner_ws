// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cleaner_msgs:msg/PlanCommand.idl
// generated code does not contain a copyright notice

#ifndef CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__BUILDER_HPP_
#define CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cleaner_msgs/msg/detail/plan_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cleaner_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanCommand_plan_json
{
public:
  explicit Init_PlanCommand_plan_json(::cleaner_msgs::msg::PlanCommand & msg)
  : msg_(msg)
  {}
  ::cleaner_msgs::msg::PlanCommand plan_json(::cleaner_msgs::msg::PlanCommand::_plan_json_type arg)
  {
    msg_.plan_json = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cleaner_msgs::msg::PlanCommand msg_;
};

class Init_PlanCommand_mission_id
{
public:
  explicit Init_PlanCommand_mission_id(::cleaner_msgs::msg::PlanCommand & msg)
  : msg_(msg)
  {}
  Init_PlanCommand_plan_json mission_id(::cleaner_msgs::msg::PlanCommand::_mission_id_type arg)
  {
    msg_.mission_id = std::move(arg);
    return Init_PlanCommand_plan_json(msg_);
  }

private:
  ::cleaner_msgs::msg::PlanCommand msg_;
};

class Init_PlanCommand_stamp
{
public:
  Init_PlanCommand_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanCommand_mission_id stamp(::cleaner_msgs::msg::PlanCommand::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_PlanCommand_mission_id(msg_);
  }

private:
  ::cleaner_msgs::msg::PlanCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cleaner_msgs::msg::PlanCommand>()
{
  return cleaner_msgs::msg::builder::Init_PlanCommand_stamp();
}

}  // namespace cleaner_msgs

#endif  // CLEANER_MSGS__MSG__DETAIL__PLAN_COMMAND__BUILDER_HPP_
