// SPDX-FileCopyrightText: 2020 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2020 Rafael de Santiago <r.santiago@ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use ket::*;

fn main() -> ket::error::Result<()> {
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
