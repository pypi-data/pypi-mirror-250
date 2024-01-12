# RL_MGM (reinforcement learning micro-gird managers) Module:
> A set of modules that can be used to aid in simulating a micro-grid environment for training reinforcement learning based energy management policy generators. The two main modules are the _DATAGENERATORS and MG_Managers. They are described in the [General information](#general-info) section below.

## Table of Contents
- [RL\_MGM (reinforcement learning micro-gird managers) Module:](#rl_mgm-reinforcement-learning-micro-gird-managers-module)
  - [Table of Contents](#table-of-contents)
  - [General Info](#general-info)
    - [\* \_DATAGENERATORS: set of tools to create stochastic data generators that represent hourly load profiles and month/hour PV MW outputs.](#-_datagenerators-set-of-tools-to-create-stochastic-data-generators-that-represent-hourly-load-profiles-and-monthhour-pv-mw-outputs)
    - [\* MG\_Managers: set of RL networks that can be trained on simulated microgrid data to generate energy management policies.](#-mg_managers-set-of-rl-networks-that-can-be-trained-on-simulated-microgrid-data-to-generate-energy-management-policies)
    - [\* MG\_Environments: tools that take a RL agent as a manager and simulate using them in the environment](#-mg_environments-tools-that-take-a-rl-agent-as-a-manager-and-simulate-using-them-in-the-environment)
  - [Technologies](#technologies)
  - [Installation](#installation)
  - [Usage](#usage)
    - [RL agent generation](#rl-agent-generation)
    - [Data Generation Tools](#data-generation-tools)
    - [](#)
  - [License](#license)

## General Info
> This rl-migrogrid-mangers (reinforcement learning) module contains a set of submodules that define RL networks for use as energy management agents, tools to generate hourly building load and various MW sizes of PV output based on the month and hour based on fitted distributions. The modules can be defined as follows:
### * _DATAGENERATORS: set of tools to create stochastic data generators that represent hourly load profiles and month/hour PV MW outputs. 
### * MG_Managers: set of RL networks that can be trained on simulated microgrid data to generate energy management policies.

### * MG_Environments: tools that take a RL agent as a manager and simulate using them in the environment

## Technologies
List the technologies used in this project. For example:
* Python: 3.8
* numpy: 1.26.3
* pandas: 2.1.4
* Joblib: 1.3.2
* matplotlib: 3.8.2
* torch: 2.1.2
* distfit: 1.7.3

## Installation
pip install rl-microgrid-managers

## Usage
### RL agent generation
### Data Generation Tools
### 



## License
MIT License

Copyright (c) <2023> <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next paragraph) shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.