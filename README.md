# DFA Sentry: Autonomous Agentic Sentry Simulation

A formal approach to autonomous agent behavior using **Deterministic Finite Automata (DFA)**. This project demonstrates how to replace complex procedural `if-else` logic with a mathematically rigid 5-tuple model to ensure 100% deterministic behavior in a real-time simulation.

## 🚀 Overview
Traditional game AI often suffers from "state-bleeding" where overlapping conditions cause agents to glitch or freeze. This simulation uses a formal **DFA** to govern a Sentry agent guarding a treasure. By discretizing the environment into a symbolic alphabet, we eliminate undefined behaviors.

## 🧠 The Formal Model
The agent is defined by the 5-tuple M = (Q, Sigma, delta, q0, F):

* **States (Q):** `Patrol`, `Chase`, `Catch`
* **Alphabet (Sigma):** `f` (Far), `n` (Near), `t` (Touch)
* **Initial State (q0):** `Patrol`
* **Final State (F):** `Catch` (A terminal trap state)
* **Transition Function (delta):** Defined via a centralized lookup table (Python dictionary).

## 🛠️ Implementation Details
- **Environment:** Built using `Pygame`.
- **Virtual Sensing:** Coordinate geometry translates distance into formal symbols (Sigma).
- **Behaviors:** - **Patrol:** Trigonometric orbiting (cos/sin) around the objective.
    - **Chase:** Vector-based pursuit tracking.
    - **Trap State:** The `Catch` state is terminal, ensuring system stability upon mission completion.



## 📁 Repository Structure
```text
├── main.py            # Main Pygame simulation and DFA logic
├── research_paper.pdf # Full technical documentation
└── README.md          # Project overview
