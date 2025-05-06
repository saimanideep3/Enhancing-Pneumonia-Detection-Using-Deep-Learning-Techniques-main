# model_training.py
from data_preprocessing import train_generator, val_generator
from model_building import model

# Model Training
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)
