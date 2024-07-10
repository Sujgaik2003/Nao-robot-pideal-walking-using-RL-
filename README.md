# LearningHumanoidWalking


## Code structure:
A rough outline for the repository that might be useful for adding your own robot:
```
LearningHumanoidWalking/
├── envs/                <-- Actions and observation space, PD gains, simulation step, control decimation, init, ...
├── tasks/               <-- Reward function, termination conditions, and more...
├── rl/                  <-- Code for PPO, actor/critic networks, observation normalization process...
├── models/              <-- MuJoCo model files: XMLs/meshes/textures
├── trained/             <-- Contains pretrained model for JVRC
└── scripts/             <-- Utility scripts, etc.
```

## Requirements:
- Python version: 3.7.11  
- [Pytorch](https://pytorch.org/)
- pip install:
  - mujoco==2.2.0
  - [mujoco-python-viewer](https://github.com/rohanpsingh/mujoco-python-viewer)
  - ray==1.9.2
  - transforms3d
  - matplotlib
  - scipy

## Usage:

Environment names supported:  

| Task Description      | Environment name |
| ----------- | ----------- |
| Basic Walking Task   | 'jvrc_walk' |
| Stepping Task (using footsteps)  | 'jvrc_step' |


#### **To train:** 

```
$ python run_experiment.py train --logdir <path_to_exp_dir> --num_procs <num_of_cpu_procs> --env <name_of_environment>
```  


#### **To play:**

We need to write a script specific to each environment.    
For example, `debug_stepper.py` can be used with the `jvrc_step` environment.  
```
$ PYTHONPATH=.:$PYTHONPATH python scripts/debug_stepper.py --path <path_to_exp_dir>
```

#### **What you should see:**

*Ascending stairs:*  

https://github.com/Sujgaik2003/Nao-robot-pideal-walking-using-RL-/assets/118328948/95fe8a74-f10a-411a-a4b9-e1019f8cfeeb


*Descending stairs:*  

https://github.com/Sujgaik2003/Nao-robot-pideal-walking-using-RL-/assets/118328948/a00de9bc-2e9e-42e1-915e-1796cfae448c


*Walking on curves:*  

https://github.com/Sujgaik2003/Nao-robot-pideal-walking-using-RL-/assets/118328948/ea4df1d8-b566-4cdc-850b-9bdf5a2fd364



```
