import numpy as np
import pandas as pd
import hssm
hssm.set_floatX("float32")

def run_ddm(drift_rate = 1,
            threshold = 1,
            starting_point = 0.5,
            noise_std = 1,
            non_decision_time = 0,
            dt = 0.01,
            max_time = 200):
    """
    Simulates the Drift Diffusion Model for one run with fixed time increments to match evidence points.

    Parameters are the same as the previous function.

    Arguments:
    - drift_rate: rate of evidence accumulation
    - threshold: evidence needed to reach a decision
    - starting_point: initial condition of the evidence
    - noise_std: standard deviation of the noise term
    - non_decision_time: time not included in the evidence accumulation process
    - dt: time increment
    - max_time: maximum simulation time

    Returns:
    - decision_time: the time taken to reach a decision
    - evidence_over_time: the evidence accumulated over time
    - decision: 1 if the decision boundary reached is the upper threshold, -1 if lower
    """
    # Initialize evidence accumulation process
    time = non_decision_time
    evidence = starting_point
    evidence_over_time = [evidence]

    # Run the simulation until a decision boundary is reached or max time is exceeded
    while time < max_time:
        # Increment the evidence by the drift and some noise
        evidence += drift_rate * dt + np.sqrt(dt) * noise_std * np.random.normal() # THERE IS A BUG IN THIS LINE
        # evidence += drift_rate + dt + np.sqrt(dt) * noise_std * np.random.normal()
        evidence_over_time.append(evidence)
        time += dt  # Increment the time

        # Check if the evidence has reached either threshold
        if evidence >= threshold: # THERE IS A BUG IN THIS LINE
            return time, evidence_over_time, 1  # Decision made for the upper threshold
        elif evidence <= 0:
            return time, evidence_over_time, -1  # Decision made for the lower threshold

    # If no decision has been made by max_time, return the current state
    return time, evidence_over_time, 0

def test_run_ddm(run_ddm_student):

    drift_rate = 1,
    threshold = 1,
    starting_point = 0.5,
    noise_std = 1,
    non_decision_time = 0,
    dt = 0.01,
    max_time = 200

    np.random.seed(0)
    decision_time, evidence_over_time, decision = run_ddm(drift_rate=v,
                                                          threshold=a,
                                                          starting_point=z,
                                                          noise_std=sigma,
                                                          non_decision_time=t0,
                                                          dt=dt,
                                                          max_time=max_time)

    np.random.seed(0)
    student_decision_time, student_evidence_over_time, student_decision = run_ddm_student(drift_rate=v,
                                                                                         threshold=a,
                                                                                         starting_point=z,
                                                                                         noise_std=sigma,
                                                                                         non_decision_time=t0,
                                                                                         dt=dt,
                                                                                         max_time=max_time)

    if not np.allclose(decision_time, student_decision_time, atol=0.01):
        print("Your run_ddm function generates incorrect outputs. Check for mistakes.")
    else:
        print("Your run_ddm function generates correct outputs!")
