
# 🌟 Life Journey FSM in Verilog

This fun Verilog project showcases a personal life journey as a finite state machine (FSM). From undergrad beginnings to industry milestones and onward to future aspirations, each state in the FSM represents a significant step in life.

---

## 🎯 Project Overview

This is a **Moore FSM** where:
- Each state represents a major phase of life.
- A single input signal `advance` takes the FSM to the next state.
- Outputs depend solely on the current state.

---
## 📊 Visual Representation

![FSM Diagram](https://github.com/VLSI-Shubh/Life-story-FSM/blob/5fed759941d917325a09e66d253d3a06da31f014/images/life_fsm.png)

---
## 🛠️ Inputs and Outputs

### Inputs
- `clk` — Clock signal
- `reset` — Asynchronous reset signal
- `advance` — Triggers transition to the next state

### Output
- `state_out` — A 3-bit signal indicating the current life state

---

## 📘 Life States

| State | Code | Description                                  |
|-------|------|----------------------------------------------|
| S0    | 0    | Undergrad in Electrical Engineering (2015)   |
| S1    | 1    | Senior Design Engineer – Oil & Gas (2019)    |
| S2    | 2    | Electrical Manager – Marine Industry (2021)  |
| S3    | 3    | Moved to US for Masters at Purdue (2023)     |
| S4    | 4    | Graduated from Purdue University (2025)      |
| S5    | 5    | Embracing VLSI & Engineering Innovation      |

---

## 💻 Project Files

| File                  | Description                                |
|-----------------------|--------------------------------------------|
| `life.v`              | Verilog FSM module                         |
| `life_fsm_tb.v`       | Testbench with realistic transitions       |
| `run_sim.sh`          | Bash script to compile and simulate        |

---


## 🧪 Simulation Output

![FSM Output](https://github.com/VLSI-Shubh/Life-story-FSM/blob/36047491e4b6633c4ea63f913c88de8671152b1a/images/simulation%20result%20_gif.gif)
---

## 📘 FSM Design (Schematic View)

The schematic below provides a hardware-level view of the FSM. It was generated via **Vivado** and **EDA Playground** and highlights:

- State transition logic  
- Register/flip-flop placement  
- Combinational & sequential logic blocks



![FSM Schematic](https://github.com/VLSI-Shubh/Life-story-FSM/blob/efdd9ce0ab466e40ec4baadec47a6037e313f0af/images/schematic.jpg)

📄 [View Full PDF Schematic](https://github.com/VLSI-Shubh/Life-story-FSM/blob/9c4d31c121e3a556cfebf0240adac14fac901c84/schematic.pdf)

---

## 🛠️ Tools Used

| Tool               | Purpose                                           |
|--------------------|---------------------------------------------------|
| **Icarus Verilog** | Compile/simulate Verilog code                    |
| **GTKWave**        | View simulation waveform dumps (`.vcd` files)    |
| **EDA Playground** | Online Verilog editor and schematic viewer       |
| **Vivado**         | RTL synthesis, schematic generation              |

---

## 🎁 Fun Factor

This project was built purely for personal exploration and enjoyment. It combines storytelling with digital design, serving as a way to test and reinforce understanding of FSM concepts in Verilog — not to teach, but to playfully challenge oneself.

---

## 📝 License

This project is licensed under the terms of the [MIT License](https://github.com/VLSI-Shubh/Life-story-FSM/blob/9c4d31c121e3a556cfebf0240adac14fac901c84/License.txt).
