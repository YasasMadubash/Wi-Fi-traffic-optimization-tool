import joblib

# Load the random forest model
model = joblib.load('random_forest_model.joblib')

# Print the model to inspect it
print(model)

# Inspect specific attributes of the model with checks
if hasattr(model, 'estimators_'):
    print(f"Number of trees in the forest: {len(model.estimators_)}")
else:
    print("The model does not have 'estimators_' attribute")

if hasattr(model, 'n_features_in_'):
    print(f"Number of features considered: {model.n_features_in_}")
else:
    print("The model does not have 'n_features_in_' attribute")

if hasattr(model, 'classes_'):
    print(f"Classes: {model.classes_}")
else:
    print("The model does not have 'classes_' attribute")

# To see a detailed summary of the model
from pprint import pprint
pprint(model.get_params())
