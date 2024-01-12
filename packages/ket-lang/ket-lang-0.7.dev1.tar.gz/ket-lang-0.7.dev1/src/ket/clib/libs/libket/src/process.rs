// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use log::info;

use crate::{
    error::{KetError, Result},
    ir::{Instruction, Metadata, PauliHamiltonian, ProcessStatus, QuantumGate, ResultData},
    objects::{Configuration, Dump, ExpValue, Measurement, QubitStatus, Sample},
};

/// Represents a quantum process.
pub struct Process {
    /// Metrics associated with the process.
    metadata: Metadata,

    /// Features associated with the process.
    config: Configuration,

    /// The quantum circuit
    instructions: Vec<Instruction>,

    /// Control stack for managing nested control scopes.
    ctrl_stack: Vec<Vec<usize>>,
    ctrl_list: Vec<usize>,
    ctrl_list_is_up_to_date: bool,

    /// Inverse instructions stack for managing nested inverse scopes.
    adj_stack: Vec<Vec<Instruction>>,

    /// List of futures associated with the process.
    measurements: Vec<Measurement>,

    /// List of expected values
    exp_values: Vec<ExpValue>,

    samples: Vec<Sample>,

    /// List of dump data associated with the process.
    dumps: Vec<Dump>,

    qubit_allocated: usize,
    qubits: Vec<QubitStatus>,
}

impl Process {
    /// Creates a new `Process` with the specified process ID, using default values for other fields.
    ///
    /// # Arguments
    ///
    /// * `pid` - The process ID.
    ///
    /// # Returns
    ///
    /// A new `Process` instance.
    pub fn new(config: Configuration) -> Self {
        Self {
            metadata: Default::default(),
            config,
            instructions: Default::default(),
            ctrl_stack: Default::default(),
            ctrl_list: Default::default(),
            ctrl_list_is_up_to_date: Default::default(),
            adj_stack: Default::default(),
            measurements: Default::default(),
            exp_values: Default::default(),
            samples: Default::default(),
            dumps: Default::default(),
            qubit_allocated: Default::default(),
            qubits: Default::default(),
        }
    }

    fn get_control_qubits(&mut self) -> &[usize] {
        if !self.ctrl_list_is_up_to_date {
            self.ctrl_list_is_up_to_date = true;
            self.ctrl_list = Vec::new();
            for inner_ctrl in self.ctrl_stack.iter() {
                self.ctrl_list.extend(inner_ctrl.iter());
            }
        }
        &self.ctrl_list
    }

    fn assert_target_not_in_control(&mut self, target: usize) -> Result<()> {
        if self.get_control_qubits().contains(&target) {
            Err(KetError::TargetInControl)
        } else {
            Ok(())
        }
    }

    fn assert_qubit_allocated(&self, qubit: usize) -> Result<()> {
        let qubit = self.qubits.get(qubit);
        match qubit {
            Some(qubit) => {
                if !qubit.allocated {
                    Err(KetError::DeallocatedQubit)
                } else {
                    Ok(())
                }
            }
            None => Err(KetError::QubitIndexOutOfBounds),
        }
    }

    fn assert_not_ready_for_execution(&self) -> Result<()> {
        if let ProcessStatus::Building = self.metadata.status {
            Ok(())
        } else {
            Err(KetError::ProcessReadyToExecute)
        }
    }

    fn assert_not_adj(&self) -> Result<()> {
        if self.adj_stack.is_empty() {
            Ok(())
        } else {
            Err(KetError::NonGateInstructionInAdj)
        }
    }

    /// Allocates a qubit in the current process.
    ///
    /// # Arguments
    ///
    /// * `dirty` - A flag indicating whether the allocated qubit can be in a dirty state.
    ///
    /// # Returns
    ///
    /// A result containing the allocated `Qubit` if successful, or an error if allocation fails.
    /// Possible error variants include `KetError::DirtyNotAllowed` if dirty qubits are not allowed,
    /// and other errors related to instruction addition or qubit management.
    ///
    pub fn allocate_qubit(&mut self) -> Result<usize> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;
        if self.qubit_allocated >= self.config.num_qubits {
            return Err(KetError::NumberOfQubitsExceeded);
        }

        let index = self.qubits.len();
        self.qubits.push(Default::default());

        self.qubit_allocated += 1;

        if self.qubit_allocated > self.metadata.qubit_simultaneous {
            self.metadata.qubit_simultaneous = self.qubit_allocated;
        }

        self.instructions.push(Instruction::Alloc { target: index });

        if let Some(processor) = self.config.live_quantum_execution.as_mut() {
            processor.alloc(index);
        }

        Ok(index)
    }

    /// Frees a previously allocated qubit in the current process.
    ///
    /// # Arguments
    ///
    /// * `qubit` - A mutable reference to the qubit to be freed.
    /// * `dirty` - A flag indicating whether the qubit should be freed in a dirty state.
    ///
    /// # Returns
    ///
    /// A result indicating the success or failure of the operation.
    /// Possible error variants include `KetError::DirtyNotAllowed` if dirty qubits are not allowed,
    /// `KetError::FreeNotAllowed` if freeing qubits is not allowed,
    /// and other errors related to instruction addition or qubit management.
    ///
    pub fn free_qubit(&mut self, qubit: usize) -> Result<()> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;
        self.assert_qubit_allocated(qubit)?;

        self.instructions.push(Instruction::Free { target: qubit });

        self.qubits[qubit].allocated = false;

        if let Some(processor) = self.config.live_quantum_execution.as_mut() {
            processor.free(qubit);
        }

        Ok(())
    }

    /// Applies a quantum gate to a target qubit in the current process.
    ///
    /// # Arguments
    ///
    /// * `gate` - The quantum gate to be applied.
    /// * `target` - A reference to the target qubit.
    ///
    /// # Returns
    ///
    /// A result indicating the success or failure of the operation.
    /// Possible error variants include `KetError::QubitNotAllocated` if the target qubit is not allocated,
    /// `KetError::PidMismatch` if the target qubit belongs to a different process,
    /// `KetError::TargetInControl` if the target qubit is also a control qubit,
    /// and other errors related to instruction addition or gate decomposition.
    ///
    pub fn apply_gate(&mut self, gate: QuantumGate, target: usize) -> Result<()> {
        self.assert_not_ready_for_execution()?;
        self.assert_qubit_allocated(target)?;
        self.assert_target_not_in_control(target)?;
        let control = self.get_control_qubits().to_vec();

        if self.config.decompose {
            todo!();
        }

        let add_adj_gate = self.adj_stack.len() % 2 == 1;

        let gate = if add_adj_gate { gate.inverse() } else { gate };

        if !self.adj_stack.is_empty() {
            self.adj_stack.last_mut().unwrap().push(Instruction::Gate {
                gate,
                target,
                control,
            });
        } else {
            if let Some(processor) = self.config.live_quantum_execution.as_mut() {
                info!(
                    "live execution: gate={:?}, target={}, control={:?}",
                    gate, target, control
                );

                processor.gate(&gate, target, &control)
            }

            self.instructions.push(Instruction::Gate {
                gate,
                target,
                control,
            });
        }

        Ok(())
    }

    /// Measures the specified qubits in the current process.
    ///
    /// # Arguments
    ///
    /// * `qubits` - An array of mutable references to the qubits to be measured.
    ///
    /// # Returns
    ///
    /// A result containing a `Future` representing the measurement result if successful, or an error if measurement fails.
    /// Possible error variants include `KetError::MeasureNotAllowed` if measuring qubits is not allowed,
    /// `KetError::PidMismatch` if any of the qubits belong to a different process,
    /// `KetError::DeallocatedQubit` if a qubit is not allocated,
    /// and other errors related to instruction addition or future creation.
    ///
    pub fn measure(&mut self, qubits: &[usize]) -> Result<usize> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;
        if !self.config.allow_measure {
            return Err(KetError::MeasureNotAllowed);
        }

        for qubit in qubits {
            self.assert_qubit_allocated(*qubit)?;
            self.qubits[*qubit].measured = true;
        }

        if !self.config.valid_after_measure {
            for qubit in qubits {
                self.qubits[*qubit].allocated = false;
            }
        }

        let measure_index = self.measurements.len();

        let result = self
            .config
            .live_quantum_execution
            .as_mut()
            .map(|processor| processor.measure(qubits));

        self.measurements.push(Measurement {
            qubits: qubits.to_vec(),
            result,
        });

        self.instructions.push(Instruction::Measure {
            qubits: qubits.to_vec(),
            output: measure_index,
        });

        Ok(measure_index)
    }

    pub fn exp_values(&mut self, hamiltonian: PauliHamiltonian) -> Result<usize> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;

        if !self.config.allow_exp_value {
            return Err(KetError::ExpValueNotAllowed);
        }

        for term in hamiltonian.products.iter().flat_map(|terms| terms.iter()) {
            self.assert_qubit_allocated(term.qubit)?;
        }

        let index = self.exp_values.len();

        let result = self
            .config
            .live_quantum_execution
            .as_mut()
            .map(|processor| processor.exp_value(&hamiltonian));

        self.exp_values.push(ExpValue {
            hamiltonian: hamiltonian.clone(),
            result,
        });

        self.instructions.push(Instruction::ExpValue {
            hamiltonian,
            output: index,
        });

        if !self.config.continue_after_exp_value {
            self.prepare_for_execution()?;
        }

        Ok(index)
    }

    pub fn sample(&mut self, qubits: &[usize], shots: u64) -> Result<usize> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;

        if !self.config.allow_sample {
            return Err(KetError::SampleNotAllowed);
        }

        for qubit in qubits {
            self.assert_qubit_allocated(*qubit)?;
        }

        let index = self.samples.len();

        let result = self
            .config
            .live_quantum_execution
            .as_mut()
            .map(|processor| processor.sample(qubits, shots));

        self.samples.push(Sample {
            qubits: qubits.to_vec(),
            shots,
            result,
        });

        self.instructions.push(Instruction::Sample {
            qubits: qubits.to_vec(),
            shots,
            output: index,
        });

        if !self.config.continue_after_exp_value {
            self.prepare_for_execution()?;
        }

        Ok(index)
    }

    /// Dumps the state of the specified qubits.
    ///
    /// # Arguments
    ///
    /// * `qubits` - The mutable references to the qubits to be dumped.
    ///
    /// # Returns
    ///
    /// A result containing a new dump object if dumping is allowed by the features,
    /// or an error (`KetError::DumpNotAllowed`) if dumping is not allowed.
    ///
    pub fn dump(&mut self, qubits: &[usize]) -> Result<usize> {
        self.assert_not_adj()?;
        self.assert_not_ready_for_execution()?;

        if !self.config.allow_dump {
            return Err(KetError::DumpNotAllowed);
        }

        for qubit in qubits {
            self.assert_qubit_allocated(*qubit)?;
        }

        let dump_index = self.dumps.len();

        let result = self
            .config
            .live_quantum_execution
            .as_mut()
            .map(|processor| processor.dump(qubits));

        self.dumps.push(Dump {
            qubits: qubits.to_vec(),
            result,
        });

        self.instructions.push(Instruction::Dump {
            qubits: qubits.to_vec(),
            output: dump_index,
        });

        if !self.config.continue_after_dump {
            self.prepare_for_execution()?;
        }

        Ok(dump_index)
    }

    /// Pushes control qubits onto the control stack.
    ///
    /// # Arguments
    ///
    /// * `qubits` - An array of references to the control qubits.
    ///
    /// # Returns
    ///
    /// A result indicating success or an error if the control configuration is invalid.
    /// Possible error variants include `KetError::DeallocatedQubit` if any of the control qubits are not allocated,
    /// `KetError::PidMismatch` if any of the control qubits belong to a different process,
    /// and `KetError::ControlTwice` if a control qubit is included in multiple control configurations.
    ///
    pub fn ctrl_push(&mut self, qubits: &[usize]) -> Result<()> {
        self.assert_not_ready_for_execution()?;
        let qubits = qubits.to_vec();
        for ctrl_list in self.ctrl_stack.iter() {
            for qubit in &qubits {
                self.assert_qubit_allocated(*qubit)?;
                if ctrl_list.contains(qubit) {
                    return Err(KetError::ControlTwice);
                }
            }
        }

        self.ctrl_stack.push(qubits);

        self.ctrl_list_is_up_to_date = false;

        Ok(())
    }

    /// Pops the top control qubit configuration from the control stack.
    ///
    /// # Returns
    ///
    /// A result indicating success or an error if the control stack is empty (`KetError::NoCtrl`).
    ///
    pub fn ctrl_pop(&mut self) -> Result<()> {
        self.assert_not_ready_for_execution()?;
        self.ctrl_list_is_up_to_date = false;

        match self.ctrl_stack.pop() {
            Some(_) => Ok(()),
            None => Err(KetError::NoCtrl),
        }
    }

    /// Begins an adjoint block, where gates are inverted upon insertion.
    ///
    /// # Returns
    ///
    /// A result indicating success or an error if there are issues with the current block.
    /// Possible error variants include `KetError::TerminatedBlock` if the current block ended.
    ///
    pub fn adj_begin(&mut self) -> Result<()> {
        self.assert_not_ready_for_execution()?;

        self.adj_stack.push(Vec::new());
        Ok(())
    }

    /// Ends the adjoint block, reverting to normal gate insertion.
    ///
    /// # Returns
    ///
    /// A result indicating success or an error if there are issues with the current block.
    /// Possible error variants include `KetError::TerminatedBlock` if the current block ended.
    ///
    pub fn adj_end(&mut self) -> Result<()> {
        self.assert_not_ready_for_execution()?;

        if self.adj_stack.is_empty() {
            return Err(KetError::NoAdj);
        }

        if self.adj_stack.len() == 1 {
            while let Some(instruction) = self.adj_stack.last_mut().unwrap().pop() {
                if let Some(processor) = self.config.live_quantum_execution.as_mut() {
                    match &instruction {
                        Instruction::Gate {
                            gate,
                            target,
                            control,
                        } => {
                            info!(
                                "live execution: gate={:?}, target={}, control={:?}",
                                gate, target, control
                            );
                            processor.gate(gate, *target, control)
                        }
                        _ => panic!(),
                    }
                }
                self.instructions.push(instruction);
            }
            self.adj_stack.pop();
        } else {
            let mut popped = self.adj_stack.pop().unwrap();
            while let Some(instruction) = popped.pop() {
                self.adj_stack.last_mut().unwrap().push(instruction);
            }
        }

        Ok(())
    }

    pub fn prepare_for_execution(&mut self) -> Result<()> {
        if let ProcessStatus::Building = self.metadata.status {
            let mut result = None;
            if let Some(processor) = self.config.batch_execution.as_mut() {
                processor.submit_execution(&self.instructions);
                self.metadata.status = ProcessStatus::Running;
                result = Some(processor.get_result());
                self.metadata.status = ProcessStatus::Terminated;
            } else {
                self.metadata.status = ProcessStatus::Ready;
            }

            if let Some(result) = result {
                self.set_result(result)?;
            }
        }
        Ok(())
    }

    pub fn get_qubit_status(&self, qubit: usize) -> &QubitStatus {
        &self.qubits[qubit]
    }

    pub fn get_measurement(&self, index: usize) -> &Measurement {
        &self.measurements[index]
    }

    pub fn get_exp_value(&self, index: usize) -> &ExpValue {
        &self.exp_values[index]
    }

    pub fn get_sample(&self, index: usize) -> &Sample {
        &self.samples[index]
    }

    pub fn get_dump(&self, index: usize) -> &Dump {
        &self.dumps[index]
    }

    /// Returns a reference to the metrics of the quantum code.
    ///
    /// # Returns
    ///
    /// A reference to the `Metrics` struct containing various metrics of the quantum code.
    ///
    pub fn get_metadata(&self) -> &Metadata {
        &self.metadata
    }

    /// Sets the result of the quantum code execution.
    ///
    /// # Arguments
    ///
    /// * `result` - The result data containing the future values, dump values, and execution time.
    ///
    /// # Returns
    ///
    /// A `Result` indicating success (`Ok`) or an error (`Err`) if the result data is unexpected.
    ///
    pub fn set_result(&mut self, mut results: ResultData) -> Result<()> {
        if self.measurements.len() != results.measurements.len()
            || self.exp_values.len() != results.exp_values.len()
            || self.samples.len() != results.samples.len()
            || self.dumps.len() != results.dumps.len()
        {
            return Err(KetError::UnexpectedResultData);
        }
        results
            .measurements
            .drain(..)
            .zip(self.measurements.iter_mut())
            .for_each(|(result, measurement)| {
                measurement.result = Some(result);
            });

        results
            .exp_values
            .drain(..)
            .zip(self.exp_values.iter_mut())
            .for_each(|(result, exp_value)| {
                exp_value.result = Some(result);
            });

        results
            .samples
            .drain(..)
            .zip(self.samples.iter_mut())
            .for_each(|(result, sample)| {
                assert_eq!(result.0.len(), result.1.len());
                sample.result = Some(result);
            });

        results
            .dumps
            .drain(..)
            .zip(self.dumps.iter_mut())
            .for_each(|(result, dump)| {
                dump.result = Some(result);
            });

        self.metadata.execution_time = results.execution_time;

        self.metadata.status = ProcessStatus::Terminated;
        Ok(())
    }

    pub(crate) fn instructions_json(&self) -> String {
        serde_json::to_string(&self.instructions).unwrap()
    }

    pub(crate) fn metadata_json(&self) -> String {
        serde_json::to_string(&self.metadata).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use crate::ir::Angle;

    use super::*;

    #[test]
    fn bell_state() -> Result<()> {
        let feature = Configuration::new(2);
        let mut process = Process::new(feature);
        let qubit_a = process.allocate_qubit()?;
        let qubit_b = process.allocate_qubit()?;

        process.apply_gate(QuantumGate::Hadamard, qubit_a)?;
        process.ctrl_push(&[qubit_a])?;
        process.apply_gate(QuantumGate::RotationX(Angle::pi()), qubit_b)?;
        process.ctrl_pop()?;

        let m_a = process.measure(&[qubit_a])?;
        let m_b = process.measure(&[qubit_b])?;

        process.prepare_for_execution()?;

        process.set_result(ResultData {
            measurements: vec![1, 1],
            exp_values: vec![],
            samples: vec![],
            dumps: vec![],
            execution_time: None,
        })?;

        println!("{:?}", process.get_measurement(m_a));
        println!("{:?}", process.get_measurement(m_b));

        Ok(())
    }
}
