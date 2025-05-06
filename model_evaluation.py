# model_evaluation.py
from data_preprocessing import test_generator
from model_building import model

# Model Evaluation
model.evaluate(test_generator)
