// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use std::{error::Error, fmt::Display, result};

#[derive(Debug, Clone, Copy)]
#[repr(i32)]
pub enum KetError {
    Success,
    ControlTwice,
    DataNotAvailable,
    DeallocatedQubit,
    QubitIndexOutOfBounds,
    NumberOfQubitsExceeded,
    NoAdj,
    NoCtrl,
    NonGateInstructionInAdj,
    TargetInControl,
    ProcessReadyToExecute,
    UnexpectedResultData,
    DumpNotAllowed,
    ExpValueNotAllowed,
    SampleNotAllowed,
    MeasureNotAllowed,
    SmallBufferSize,
    UndefinedError,
}

pub type Result<T> = result::Result<T, KetError>;

impl KetError {
    pub fn to_str(&self) -> &'static str {
        match self {
            KetError::Success => "The operation completed successfully.",
            KetError::ControlTwice => "Cannot set a qubit as a control twice.",
            KetError::DeallocatedQubit => "Cannot operate with a deallocated qubit.",
            KetError::NoAdj => "No inverse scope to end.",
            KetError::NoCtrl => "No control scope to end.",
            KetError::NonGateInstructionInAdj => {
                "Cannot apply a non-gate instruction within a controlled or inverse scope."
            }
            KetError::TargetInControl => {
                "A qubit cannot be both targeted and controlled at the same time."
            }
            KetError::ProcessReadyToExecute => "Cannot append statements to a terminated process.",
            KetError::UnexpectedResultData => {
                "Result does not contain the expected number of values."
            }
            KetError::UndefinedError => "An undefined error occurred.",
            KetError::DataNotAvailable => "Requested data is not available.",
            KetError::DumpNotAllowed => "Cannot dump qubits (feature disabled).",
            KetError::MeasureNotAllowed => "Cannot measure qubit (feature disabled).",
            KetError::QubitIndexOutOfBounds => "The provided qubit index is out of bounds.",
            KetError::NumberOfQubitsExceeded => "The number of qubits exceeds the allowed limit.",
            KetError::ExpValueNotAllowed => {
                "Cannot calculate the expected value (feature disabled)."
            }
            KetError::SampleNotAllowed => "Cannot sampling qubits (feature disabled).",
            KetError::SmallBufferSize => "The provided buffer is too small.",
        }
    }

    pub fn error_code(&self) -> i32 {
        *self as i32
    }

    pub fn from_error_code(error_code: i32) -> KetError {
        unsafe { std::mem::transmute(error_code) }
    }
}

impl Display for KetError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.to_str())
    }
}

impl Error for KetError {}

#[cfg(test)]
mod tests {
    use super::KetError;

    #[test]
    fn success_is_zero() {
        assert!(KetError::Success.error_code() == 0)
    }

    #[test]
    fn print_error_code() {
        let mut error_code = 0;
        loop {
            let error = KetError::from_error_code(error_code);
            let error_str = format!("{:#?}", error);
            let error_str = error_str
                .split_inclusive(char::is_uppercase)
                .map(|part| {
                    let size = part.len();
                    let lest = part.chars().last().unwrap();
                    if size > 1 && char::is_uppercase(lest) {
                        format!("{}_{}", &part[..size - 1], lest)
                    } else {
                        String::from(part)
                    }
                })
                .collect::<Vec<String>>()
                .concat()
                .to_uppercase();
            println!("#define KET_{} {}", error_str, error_code);

            if let KetError::UndefinedError = error {
                break;
            } else {
                error_code += 1;
            }
        }
    }
}
