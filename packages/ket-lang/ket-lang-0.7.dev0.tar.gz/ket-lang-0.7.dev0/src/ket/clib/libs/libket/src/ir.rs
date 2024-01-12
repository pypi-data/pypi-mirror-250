// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use std::collections::HashMap;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DumpData {
    pub basis_states: Vec<Vec<u64>>,
    pub amplitudes_real: Vec<f64>,
    pub amplitudes_imag: Vec<f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Angle {
    Scalar(f64),
    PiFraction { top: i32, bottom: u32 },
}

impl Angle {
    pub fn inverse(&self) -> Angle {
        match self {
            Angle::Scalar(angle) => Angle::Scalar(-angle),
            Angle::PiFraction { top, bottom } => Angle::PiFraction {
                top: -top,
                bottom: *bottom,
            },
        }
    }

    pub fn pi() -> Angle {
        Angle::PiFraction { top: 1, bottom: 1 }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum QuantumGate {
    PauliX,
    PauliY,
    PauliZ,
    RotationX(Angle),
    RotationY(Angle),
    RotationZ(Angle),
    Phase(Angle),
    Hadamard,
}

impl QuantumGate {
    pub fn inverse(&self) -> QuantumGate {
        match self {
            QuantumGate::RotationX(angle) => QuantumGate::RotationX(angle.inverse()),
            QuantumGate::RotationY(angle) => QuantumGate::RotationY(angle.inverse()),
            QuantumGate::RotationZ(angle) => QuantumGate::RotationZ(angle.inverse()),
            QuantumGate::Phase(angle) => QuantumGate::Phase(angle.inverse()),
            QuantumGate::Hadamard => QuantumGate::Hadamard,
            QuantumGate::PauliX => QuantumGate::PauliX,
            QuantumGate::PauliY => QuantumGate::PauliY,
            QuantumGate::PauliZ => QuantumGate::PauliZ,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Pauli {
    PauliX,
    PauliY,
    PauliZ,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PauliTerm {
    pub pauli: Pauli,
    pub qubit: usize,
}

pub type PauliProduct = Vec<PauliTerm>;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct PauliHamiltonian {
    pub products: Vec<PauliProduct>,
    pub coefficients: Vec<f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Instruction {
    Alloc {
        target: usize,
    },
    Free {
        target: usize,
    },
    Gate {
        gate: QuantumGate,
        target: usize,
        control: Vec<usize>,
    },
    Measure {
        qubits: Vec<usize>,
        output: usize,
    },
    ExpValue {
        hamiltonian: PauliHamiltonian,
        output: usize,
    },
    Sample {
        qubits: Vec<usize>,
        shots: u64,
        output: usize,
    },
    Dump {
        qubits: Vec<usize>,
        output: usize,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub enum ProcessStatus {
    #[default]
    Building,
    Ready,
    Running,
    Terminated,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct Metadata {
    pub qubit_simultaneous: usize,
    pub timeout: Option<u64>,
    pub status: ProcessStatus,
    pub execution_time: Option<f64>,
    pub gate_count: HashMap<usize, usize>,
    pub depth: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct ResultData {
    pub measurements: Vec<u64>,
    pub exp_values: Vec<f64>,
    pub samples: Vec<(Vec<u64>, Vec<u64>)>,
    pub dumps: Vec<DumpData>,
    pub execution_time: Option<f64>,
}
