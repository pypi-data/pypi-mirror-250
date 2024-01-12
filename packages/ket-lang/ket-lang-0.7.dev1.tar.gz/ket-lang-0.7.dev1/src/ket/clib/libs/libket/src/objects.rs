// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use crate::{
    ir::{DumpData, PauliHamiltonian, QuantumGate},
    Instruction, ResultData,
};

pub trait LiveExecution {
    fn alloc(&mut self, target: usize);
    fn free(&mut self, target: usize);
    fn gate(&mut self, gate: &QuantumGate, target: usize, control: &[usize]);
    fn measure(&mut self, qubits: &[usize]) -> u64;
    fn exp_value(&mut self, hamiltonian: &PauliHamiltonian) -> f64;
    fn sample(&mut self, qubits: &[usize], shots: u64) -> (Vec<u64>, Vec<u64>);
    fn dump(&mut self, qubits: &[usize]) -> DumpData;
}

pub enum ExecutionStatus {
    New,
    Ready,
    Running,
    Completed,
    Error,
}

pub trait BatchExecution {
    fn submit_execution(&mut self, instructions: &[Instruction]);
    fn get_result(&mut self) -> ResultData;
    fn get_status(&self) -> ExecutionStatus;
}

/// Set of features for a `Process` object.
pub struct Configuration {
    pub allow_measure: bool,
    pub allow_sample: bool,
    pub allow_exp_value: bool,
    pub allow_dump: bool,

    pub valid_after_measure: bool,

    pub continue_after_sample: bool,
    pub continue_after_exp_value: bool,
    pub continue_after_dump: bool,

    pub decompose: bool,
    pub live_quantum_execution: Option<Box<dyn LiveExecution>>,
    pub batch_execution: Option<Box<dyn BatchExecution>>,

    pub num_qubits: usize,

    pub execution_timeout: Option<f64>,
}

impl Configuration {
    pub fn new(num_qubits: usize) -> Self {
        Self {
            allow_measure: true,
            allow_sample: true,
            allow_exp_value: true,
            allow_dump: true,
            valid_after_measure: true,
            continue_after_sample: true,
            continue_after_exp_value: true,
            continue_after_dump: true,
            decompose: false,
            live_quantum_execution: None,
            batch_execution: None,
            num_qubits,
            execution_timeout: None,
        }
    }
}

#[derive(Debug, Clone)]
pub struct QubitStatus {
    pub allocated: bool,
    pub measured: bool,
}

impl Default for QubitStatus {
    fn default() -> Self {
        Self {
            allocated: true,
            measured: false,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Measurement {
    pub qubits: Vec<usize>,
    pub result: Option<u64>,
}

#[derive(Debug, Clone)]
pub struct ExpValue {
    pub hamiltonian: PauliHamiltonian,
    pub result: Option<f64>,
}

#[derive(Debug, Clone)]
pub struct Sample {
    pub qubits: Vec<usize>,
    pub shots: u64,
    pub result: Option<(Vec<u64>, Vec<u64>)>,
}

#[derive(Debug, Clone)]
pub struct Dump {
    pub qubits: Vec<usize>,
    pub result: Option<DumpData>,
}
