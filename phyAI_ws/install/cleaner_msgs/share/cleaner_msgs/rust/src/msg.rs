#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to cleaner_msgs__msg__CleanerState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CleanerState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub system_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_frame: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_yaw: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_vx: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_vy: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_wz: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub battery_soc: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub battery_voltage: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub primary_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lost_sec: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vision_json: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_json: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_index: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub queue_status: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub history_json: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub roe_ok: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub safe_backstop: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_speed: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_violation: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub events_json: std::string::String,

}



impl Default for CleanerState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CleanerState::default())
  }
}

impl rosidl_runtime_rs::Message for CleanerState {
  type RmwMsg = super::msg::rmw::CleanerState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        system_state: msg.system_state.as_str().into(),
        pose_frame: msg.pose_frame.as_str().into(),
        pose_x: msg.pose_x,
        pose_y: msg.pose_y,
        pose_yaw: msg.pose_yaw,
        vel_vx: msg.vel_vx,
        vel_vy: msg.vel_vy,
        vel_wz: msg.vel_wz,
        battery_soc: msg.battery_soc,
        battery_voltage: msg.battery_voltage,
        primary_id: msg.primary_id,
        lost_sec: msg.lost_sec,
        vision_json: msg.vision_json.as_str().into(),
        plan_json: msg.plan_json.as_str().into(),
        current_index: msg.current_index,
        queue_status: msg.queue_status.as_str().into(),
        history_json: msg.history_json.as_str().into(),
        roe_ok: msg.roe_ok,
        safe_backstop: msg.safe_backstop,
        max_speed: msg.max_speed,
        last_violation: msg.last_violation.as_str().into(),
        events_json: msg.events_json.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
        system_state: msg.system_state.as_str().into(),
        pose_frame: msg.pose_frame.as_str().into(),
      pose_x: msg.pose_x,
      pose_y: msg.pose_y,
      pose_yaw: msg.pose_yaw,
      vel_vx: msg.vel_vx,
      vel_vy: msg.vel_vy,
      vel_wz: msg.vel_wz,
      battery_soc: msg.battery_soc,
      battery_voltage: msg.battery_voltage,
      primary_id: msg.primary_id,
      lost_sec: msg.lost_sec,
        vision_json: msg.vision_json.as_str().into(),
        plan_json: msg.plan_json.as_str().into(),
      current_index: msg.current_index,
        queue_status: msg.queue_status.as_str().into(),
        history_json: msg.history_json.as_str().into(),
      roe_ok: msg.roe_ok,
      safe_backstop: msg.safe_backstop,
      max_speed: msg.max_speed,
        last_violation: msg.last_violation.as_str().into(),
        events_json: msg.events_json.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      system_state: msg.system_state.to_string(),
      pose_frame: msg.pose_frame.to_string(),
      pose_x: msg.pose_x,
      pose_y: msg.pose_y,
      pose_yaw: msg.pose_yaw,
      vel_vx: msg.vel_vx,
      vel_vy: msg.vel_vy,
      vel_wz: msg.vel_wz,
      battery_soc: msg.battery_soc,
      battery_voltage: msg.battery_voltage,
      primary_id: msg.primary_id,
      lost_sec: msg.lost_sec,
      vision_json: msg.vision_json.to_string(),
      plan_json: msg.plan_json.to_string(),
      current_index: msg.current_index,
      queue_status: msg.queue_status.to_string(),
      history_json: msg.history_json.to_string(),
      roe_ok: msg.roe_ok,
      safe_backstop: msg.safe_backstop,
      max_speed: msg.max_speed,
      last_violation: msg.last_violation.to_string(),
      events_json: msg.events_json.to_string(),
    }
  }
}


// Corresponds to cleaner_msgs__msg__PlanCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_json: std::string::String,

}



impl Default for PlanCommand {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PlanCommand::default())
  }
}

impl rosidl_runtime_rs::Message for PlanCommand {
  type RmwMsg = super::msg::rmw::PlanCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        mission_id: msg.mission_id.as_str().into(),
        plan_json: msg.plan_json.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
        mission_id: msg.mission_id.as_str().into(),
        plan_json: msg.plan_json.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      mission_id: msg.mission_id.to_string(),
      plan_json: msg.plan_json.to_string(),
    }
  }
}


// Corresponds to cleaner_msgs__msg__ReplanRequest

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReplanRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub context_json: std::string::String,

}



impl Default for ReplanRequest {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ReplanRequest::default())
  }
}

impl rosidl_runtime_rs::Message for ReplanRequest {
  type RmwMsg = super::msg::rmw::ReplanRequest;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        mission_id: msg.mission_id.as_str().into(),
        reason: msg.reason.as_str().into(),
        context_json: msg.context_json.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
        mission_id: msg.mission_id.as_str().into(),
        reason: msg.reason.as_str().into(),
        context_json: msg.context_json.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      mission_id: msg.mission_id.to_string(),
      reason: msg.reason.to_string(),
      context_json: msg.context_json.to_string(),
    }
  }
}


