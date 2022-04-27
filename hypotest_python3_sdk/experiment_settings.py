class ExperimentSettings:
    def __init__(self, experiment_id, experiment_name, experiment_hypothesis, tag_names, condition_to_enter_experiment,
                 variants_distribution, goal_names, experiment_state, experiment_active,
                 override_control, override_b):
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name
        self.experiment_hypothesis = experiment_hypothesis
        self.tag_names = tag_names
        self.condition_to_enter_experiment = condition_to_enter_experiment
        self.variants_distribution = variants_distribution
        self.goal_names = goal_names
        self.experiment_state = experiment_state
        self.experiment_active = experiment_active
        self.override_control = override_control
        self.override_b = override_b
