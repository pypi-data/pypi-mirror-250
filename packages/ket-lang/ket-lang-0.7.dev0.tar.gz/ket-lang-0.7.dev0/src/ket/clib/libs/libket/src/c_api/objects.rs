// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use log::trace;

use crate::{error::KetError, Process};

#[no_mangle]
pub extern "C" fn ket_process_get_qubit_status(
    process: &Process,
    qubit: usize,
    allocated: &mut bool,
    measured: &mut bool,
) -> i32 {
    let qubit_status = process.get_qubit_status(qubit);
    *allocated = qubit_status.allocated;
    *measured = qubit_status.measured;

    trace!("{:?}", qubit_status);

    KetError::Success.error_code()
}

#[no_mangle]
pub extern "C" fn ket_process_get_measurement(
    process: &Process,
    index: usize,
    available: &mut bool,
    result: &mut u64,
) -> i32 {
    let measurement = process.get_measurement(index);
    if let Some(measurement) = measurement.result {
        *result = measurement;
        *available = true;
    } else {
        *available = false;
    }

    trace!("{:?}", measurement);

    KetError::Success.error_code()
}

#[no_mangle]
pub extern "C" fn ket_process_get_exp_value(
    process: &Process,
    index: usize,
    available: &mut bool,
    result: &mut f64,
) -> i32 {
    let exp_value = process.get_exp_value(index);
    if let Some(exp_value) = exp_value.result {
        *result = exp_value;
        *available = true;
    } else {
        *available = false;
    }

    KetError::Success.error_code()
}

#[no_mangle]
pub extern "C" fn ket_process_get_sample(
    process: &Process,
    index: usize,
    available: &mut bool,
    result: &mut *const u64,
    count: &mut *const u64,
    size: &mut usize,
) -> i32 {
    let sample = process.get_sample(index);
    if let Some(sample) = sample.result.as_ref() {
        *result = sample.0.as_ptr();
        *count = sample.1.as_ptr();
        *size = sample.0.len();
        *available = true;
    } else {
        *available = false;
    }

    KetError::Success.error_code()
}

#[no_mangle]
pub extern "C" fn ket_process_get_dump_size(
    process: &Process,
    index: usize,
    available: &mut bool,
    size: &mut usize,
) -> i32 {
    let dump = process.get_dump(index);
    if let Some(dump) = dump.result.as_ref() {
        *size = dump.basis_states.len();
        *available = true;
    } else {
        *available = false;
    }

    KetError::Success.error_code()
}

/// Retrieves a specific basis state from the dump.
///
/// # Arguments
///
/// * `dump` - \[in\] A reference to the `Dump` instance.
/// * `index` - \[in\] The index of the basis state to retrieve.
/// * `state` - \[out\] A mutable pointer to store the basis state.
/// * `size` - \[out\] A mutable reference to store the size of the basis state.
///
/// # Returns
///
/// An integer representing the error code. `0` indicates success.
/// # Safety
///
/// This function is marked as unsafe because it deals with raw pointers.
#[no_mangle]
pub unsafe extern "C" fn ket_process_get_dump(
    process: &Process,
    index: usize,
    iterator: usize,
    basis_state: &mut *const u64,
    basis_state_size: &mut usize,
    amplitude_real: &mut f64,
    amplitude_imag: &mut f64,
) -> i32 {
    let dump = process.get_dump(index).result.as_ref().unwrap();
    let state = dump.basis_states[iterator].as_ptr();
    let size = dump.basis_states[iterator].len();
    *basis_state = state;
    *basis_state_size = size;
    *amplitude_real = dump.amplitudes_real[iterator];
    *amplitude_imag = dump.amplitudes_imag[iterator];

    KetError::Success.error_code()
}
