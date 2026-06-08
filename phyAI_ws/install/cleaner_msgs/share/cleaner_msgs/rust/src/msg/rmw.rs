#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "cleaner_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__CleanerState() -> *const std::ffi::c_void;
}

#[link(name = "cleaner_msgs__rosidl_generator_c")]
extern "C" {
    fn cleaner_msgs__msg__CleanerState__init(msg: *mut CleanerState) -> bool;
    fn cleaner_msgs__msg__CleanerState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CleanerState>, size: usize) -> bool;
    fn cleaner_msgs__msg__CleanerState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CleanerState>);
    fn cleaner_msgs__msg__CleanerState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CleanerState>, out_seq: *mut rosidl_runtime_rs::Sequence<CleanerState>) -> bool;
}

// Corresponds to cleaner_msgs__msg__CleanerState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CleanerState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub system_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_frame: rosidl_runtime_rs::String,


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
    pub vision_json: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_json: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_index: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub queue_status: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub history_json: rosidl_runtime_rs::String,


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
    pub last_violation: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub events_json: rosidl_runtime_rs::String,

}



impl Default for CleanerState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !cleaner_msgs__msg__CleanerState__init(&mut msg as *mut _) {
        panic!("Call to cleaner_msgs__msg__CleanerState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CleanerState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__CleanerState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__CleanerState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__CleanerState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CleanerState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CleanerState where Self: Sized {
  const TYPE_NAME: &'static str = "cleaner_msgs/msg/CleanerState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__CleanerState() }
  }
}


#[link(name = "cleaner_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__PlanCommand() -> *const std::ffi::c_void;
}

#[link(name = "cleaner_msgs__rosidl_generator_c")]
extern "C" {
    fn cleaner_msgs__msg__PlanCommand__init(msg: *mut PlanCommand) -> bool;
    fn cleaner_msgs__msg__PlanCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanCommand>, size: usize) -> bool;
    fn cleaner_msgs__msg__PlanCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanCommand>);
    fn cleaner_msgs__msg__PlanCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanCommand>) -> bool;
}

// Corresponds to cleaner_msgs__msg__PlanCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_json: rosidl_runtime_rs::String,

}



impl Default for PlanCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !cleaner_msgs__msg__PlanCommand__init(&mut msg as *mut _) {
        panic!("Call to cleaner_msgs__msg__PlanCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__PlanCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__PlanCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__PlanCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanCommand where Self: Sized {
  const TYPE_NAME: &'static str = "cleaner_msgs/msg/PlanCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__PlanCommand() }
  }
}


#[link(name = "cleaner_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__ReplanRequest() -> *const std::ffi::c_void;
}

#[link(name = "cleaner_msgs__rosidl_generator_c")]
extern "C" {
    fn cleaner_msgs__msg__ReplanRequest__init(msg: *mut ReplanRequest) -> bool;
    fn cleaner_msgs__msg__ReplanRequest__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReplanRequest>, size: usize) -> bool;
    fn cleaner_msgs__msg__ReplanRequest__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReplanRequest>);
    fn cleaner_msgs__msg__ReplanRequest__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReplanRequest>, out_seq: *mut rosidl_runtime_rs::Sequence<ReplanRequest>) -> bool;
}

// Corresponds to cleaner_msgs__msg__ReplanRequest
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReplanRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mission_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub context_json: rosidl_runtime_rs::String,

}



impl Default for ReplanRequest {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !cleaner_msgs__msg__ReplanRequest__init(&mut msg as *mut _) {
        panic!("Call to cleaner_msgs__msg__ReplanRequest__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReplanRequest {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__ReplanRequest__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__ReplanRequest__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { cleaner_msgs__msg__ReplanRequest__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReplanRequest {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReplanRequest where Self: Sized {
  const TYPE_NAME: &'static str = "cleaner_msgs/msg/ReplanRequest";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__cleaner_msgs__msg__ReplanRequest() }
  }
}


