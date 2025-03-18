use std::fmt::Display;
use std::fs::OpenOptions;
use std::io::prelude::*;

pub enum Attack {
    RegisterBitFlip { pc: u32, bit: u8, register: u8 },
}

impl From<&[i32]> for Attack {
    fn from(data: &[i32]) -> Self {
        match data[0] {
            0 => Attack::RegisterBitFlip {
                pc: data[1].try_into().unwrap(),
                bit: data[2].try_into().unwrap(),
                register: data[3].try_into().unwrap(),
            },
            _ => panic!("unknown attack type"),
        }
    }
}

impl Display for Attack {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Attack::RegisterBitFlip { pc, bit, register } => {
                write!(f, "RC{{pc:{}; bit:{}; register:{}}}", pc, bit, register)
            }
        }
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn log_attack_plan(
    status: u8,                     // 0: VM instruction is invalid. 1: Execution finished without a problem.
    serialised_attacks: *const i32, // The array of i32 values representing a serialised attack plan.
    length_of_attack: u16,          // The number of i32 values per attack.
    number_of_attacks: u16,         // The number of serialised attacks.
    globals: *const i32,
    globals_length: u16,
    registers: *const i32,
) {
    if serialised_attacks.is_null() || number_of_attacks == 0 {
        return;
    }

    let serialised_attacks_slice = unsafe {
        std::slice::from_raw_parts(
            serialised_attacks,
            (number_of_attacks as usize) * (length_of_attack as usize),
        )
    };

    let mut attacks: Vec<Attack> = Vec::with_capacity(number_of_attacks as usize);

    for i in 0..number_of_attacks {
        let start = (i * length_of_attack) as usize;
        let end = ((i + 1) * length_of_attack) as usize;
        let attack_slice = &serialised_attacks_slice[start..end];
        let attack = Attack::from(attack_slice);
        attacks.push(attack);
    }

    let mut file = match OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open("./attack-plans.txt")
    {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Error opening file: {}", e);
            return;
        }
    };

    if let Err(e) = write!(file, "status:{}; ", status) {
        eprintln!("Error writing to file: {}", e);
    }

    let attack_plan: Vec<String> = attacks.iter().map(Attack::to_string).collect();
    if let Err(e) = write!(file, "attack_plan:[{}]; ", attack_plan.join(", ")) {
        eprintln!("Error writing to file: {}", e);
    }

    let registers_slice = unsafe {
        std::slice::from_raw_parts(registers, 32)
    };
    let registers_strings: Vec<String> = registers_slice.iter().map(i32::to_string).collect();
    if let Err(e) = write!(file, "registers:[{}]; ", registers_strings.join(", ")) {
        eprintln!("Error writing to file: {}", e);
    }

    let globals_slice = unsafe {
        std::slice::from_raw_parts(globals, globals_length as usize)
    };
    let globals_strings: Vec<String> = globals_slice.iter().map(i32::to_string).collect();
    if let Err(e) = write!(file, "globals:[{}]", globals_strings.join(", ")) {
        eprintln!("Error writing to file: {}", e);
    }

    if let Err(e) = write!(file, "\n") {
        eprintln!("Error writing to file: {}", e);
    }
}
