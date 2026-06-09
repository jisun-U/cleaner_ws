// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cleaner_msgs:msg/ReplanRequest.idl
// generated code does not contain a copyright notice

#ifndef CLEANER_MSGS__MSG__DETAIL__REPLAN_REQUEST__BUILDER_HPP_
#define CLEANER_MSGS__MSG__DETAIL__REPLAN_REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cleaner_msgs/msg/detail/replan_request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cleaner_msgs
{

namespace msg
{

namespace builder
{

class Init_ReplanRequest_context_json
{
public:
  explicit Init_ReplanRequest_context_json(::cleaner_msgs::msg::ReplanRequest & msg)
  : msg_(msg)
  {}
  ::cleaner_msgs::msg::ReplanRequest context_json(::cleaner_msgs::msg::ReplanRequest::_context_json_type arg)
  {
    msg_.context_json = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cleaner_msgs::msg::ReplanRequest msg_;
};

class Init_ReplanRequest_reason
{
public:
  explicit Init_ReplanRequest_reason(::cleaner_msgs::msg::ReplanRequest & msg)
  : msg_(msg)
  {}
  Init_ReplanRequest_context_json reason(::cleaner_msgs::msg::ReplanRequest::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ReplanRequest_context_json(msg_);
  }

private:
  ::cleaner_msgs::msg::ReplanRequest msg_;
};

class Init_ReplanRequest_mission_id
{
public:
  explicit Init_ReplanRequest_mission_id(::cleaner_msgs::msg::ReplanRequest & msg)
  : msg_(msg)
  {}
  Init_ReplanRequest_reason mission_id(::cleaner_msgs::msg::ReplanRequest::_mission_id_type arg)
  {
    msg_.mission_id = std::move(arg);
    return Init_ReplanRequest_reason(msg_);
  }

private:
  ::cleaner_msgs::msg::ReplanRequest msg_;
};

class Init_ReplanRequest_stamp
{
public:
  Init_ReplanRequest_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ReplanRequest_mission_id stamp(::cleaner_msgs::msg::ReplanRequest::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_ReplanRequest_mission_id(msg_);
  }

private:
  ::cleaner_msgs::msg::ReplanRequest msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cleaner_msgs::msg::ReplanRequest>()
{
  return cleaner_msgs::msg::builder::Init_ReplanRequest_stamp();
}

}  // namespace cleaner_msgs

#endif  // CLEANER_MSGS__MSG__DETAIL__REPLAN_REQUEST__BUILDER_HPP_
