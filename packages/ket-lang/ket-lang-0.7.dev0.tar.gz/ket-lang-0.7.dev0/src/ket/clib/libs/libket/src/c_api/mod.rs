// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

//! # FFI Wrapper
//!
//! This module provides a wrapper for Foreign Function Interface (FFI) functions in Rust.
//! It includes utility functions for error handling and retrieving error messages,
//! as well as functions for interacting with FFI data structures.
//!
//! ## Error Handling
//!
//! The `ket_error_message` function allows retrieving error messages associated with error codes.
//! Given an error code, it returns a pointer to the corresponding error message string.
//!
//! ## FFI Data Structures
//!
//! This module also includes functions for interacting with FFI data structures such as `Features`, `Qubit`, `Dump`, `Future`, and `Label`.
//! These functions provide operations for creating, deleting, and accessing properties of these data structures in the FFI context.
//!
//! # Safety
//!
//! Care should be taken when using FFI functions and data structures.
//! Follow the provided documentation and ensure that proper memory management
//! and safety measures are followed.

use env_logger::Builder;
use log::LevelFilter;

use crate::error::KetError;

pub mod error;
pub mod objects;
pub mod process;

#[no_mangle]
pub extern "C" fn ket_set_log_level(level: u32) -> i32 {
    let level = match level {
        0 => LevelFilter::Off,
        1 => LevelFilter::Error,
        2 => LevelFilter::Warn,
        3 => LevelFilter::Info,
        4 => LevelFilter::Debug,
        5 => LevelFilter::Trace,
        _ => LevelFilter::max(),
    };

    Builder::new().filter_level(level).init();

    KetError::Success.error_code()
}
