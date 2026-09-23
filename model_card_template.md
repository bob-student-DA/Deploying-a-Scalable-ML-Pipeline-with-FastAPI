# Model Card

For additional information see the Model Card paper: https://arxiv.org/pdf/1810.03993.pdf

## Model Details
This model is a Random Forest Classifier, implemented using scikit-learn's
`RandomForestClassifier` (default hyperparameters, `random_state=42` for reproducibility). 
It was developed as part of a Udacity Machine Learning DevOps Engineer project,
"Deploying a Scalable ML Pipeline with FastAPI." 
The model was trained by Bobbie Hickman, September 2026.

## Intended Use
This model is intended to predict whether a persons annual income
exceeds $50,000 based on U.S. Census demographic and employment data. 
It is intended for educational and demonstration purposes as part of an
ML pipeline deployment practice, showing how a model can be trained, tested, and served via a REST API. 

## Training Data
The model was trained on the UCI Census Income (Adult) dataset, sourced 
from the fed `census.csv` file (32,561 rows). The dataset includes demographic 
and employment features such as age, workclass, education, marital status, 
occupation, relationship, race, sex, capital gain/loss, hours worked per week,
and native country. 80% of the data (using an 80/20 train-test split, random_state=42) 
was used for training. Categorical features were one-hot encoded, and the target label 
(salary: <=50K or >50K) was binarized.

## Evaluation Data
The remaining 20% of the dataset was held out as a test set, processed
using the same one-hot encoder and label binarizer fitted on the
training data, to ensure consistent feature modelling between
training and evaluation.

## Metrics
The model's performance was evaluated using precision, recall, and
F1 score (fbeta with beta=1). On the excluded test set, the model
achieved:
- Precision: 0.7419
- Recall: 0.6384
- F1: 0.6863

Performance was also evaluated on slices of the data for each
categorical feature (see `slice_output.txt`). Performance varied
notably across some subgroups — for example, larger groups such as
"United-States" (native-country, n=5,870) and "Private" (workclass,
n=4,578) had metrics close to the overall averages, while several
smaller subgroups (certain native-country values with fewer
than 10 samples) showed precision or recall values of exactly 0.0
or 1.0. These extreme values are presumably artifacts of small sample
size rather than reliable indicators of model performance for those
groups.

## Ethical Considerations
This dataset includes sensitive demographic attributes such as race,
sex, and native country. Because the model uses these as predictive
features, there is a risk of learning or reinforcing existing societal
biases present in the historical census data (historical income
disparities across race or sex). The slice performance analysis shows
uneven performance across some subgroups, particularly those with small sample sizes, 
which could lead to unreliable predictions for underrepresented groups. This model 
should not be used to make real decisions about individuals' income, employment, or creditworthiness.

## Caveats and Recommendations
The dataset is from historical U.S. Census data and may not reflect
current economic or demographic conditions. Some categorical slices
retain especially small sample sizes (fewer than 10 records), making their
individual performance metrics unreliable. These should be
interpreted with caution rather than as confident performance claims.
Future improvements could include collecting more balanced data across 
underrepresented subgroups to improve fairness and reliability and k-fold cross-validation 
instead of a single train/test split.
