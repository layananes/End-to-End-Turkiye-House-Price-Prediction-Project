# :star2: End-to-End Turkiye House Price Prediction Project :star2:

This project predicts house prices in Turkiye while considering many factors like area, city, room count, and floor count. 

## Table of contents 
- Dataset
- Features
- Modeling
- Evaluation
- API
- Front-end


### :+1: Overview
In the project, we were handed a raw dataset, whcih we then cleaned up and encoded. We used different models and observed their predictive accuracy, and chose the best one to apply with API and front-end simple web development. 

### Features
The features of the dataset consist of:
- Net area
- Gross area
- Room count
- Floor location	
- Building age	
- Heating type	
- City	
- Occupancy status	
- Investment eligibility	
- Title deed status	
- Bathroom count

Our file `home_price.csv` contains the old original and untouched version of our data set. File `final_cleaned_home_price_data` is our new cleaned data set. 

### Modeling
Before training our models, we had to start with data cleaning. We used codes like .info() and .describe() to view and understand our dataset. We then made sure the dataset didn't have any unknown or duplicated data, and dealt with any if found. Any outliers that may affect the model were also removed or dealt with, along with any features we deemed to be unrelated or unnecessary. 

The next step was to build our model by encoding. Since each model tends to prefer specific encoding methods, we needed to try multiple methods so we can compare and pick the best. 
The models we worked on were: 

- `LightGBM`: It is a mainly tree based model. It follows leaf-wise system and is generally better on larger data sets
- `CatBoost`: categorical based model
- `Random Forest`: Made up of many decision but different decision trees, who each vote on the      result to reach one final result
- `XGboost`: Like Random Forest, it is also made up of multiple decision trees. It works by 'boosting', where the previous mistakes of the decision trees helps influence subsequent decisions
- `Linear regression`: Builds linear relationships to try adnd fit the data

After encoding all our data to fit each specific model, we started our model training process, during which we split our data (usually a 70%-15%-15% split) before scaling any if necessary. We then called the model building codes from their libraries so we can actually finish up the model building process.

### Evaluation
In thi step, we evaluated our models to make sure they are accurate. we view their ROC-AUC if possible, as well as their training scores. 

**LightGBM** was the best with :

    Training Score:  74% 
    R² Score (Accuracy):  65.27%    
    MAE (Avg Error):      856,397 TL
    RMSE (Large Error):   1,728,076 TL

        
### API and Front-end
Using API, we were able to create a suitable and easily understandable way for the user to interact with the mode since it doesn't understand spoken language. 


