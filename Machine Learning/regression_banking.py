#Evaluating a possibility of a person repaing his debts.
#Dataset of repaid and charged off debts obtained from Kaggle and should be located
#at the same directory with this file

import random
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation,Dropout
from tensorflow.keras.constraints import max_norm



df = pd.read_csv('lending_info.csv')

########################
#DATA ANALYSIS
########################

# Total debts breakdown
sns.countplot(x='loan_status',data=df)
plt.show()

# correlation visualization
plt.figure(figsize=(12,6))
sns.heatmap(df.corr(),annot=True,cmap='viridis')
plt.ylim(10, 0)
plt.show()

#Paid and charged off debts in accordance with customers grade
plt.figure(figsize=(12,4))
subgrade_order = sorted(df['sub_grade'].unique())
sns.countplot(x='sub_grade',data=df,order = subgrade_order,palette='coolwarm' ,hue='loan_status')
plt.show()

#creating new column 'loan repaid' with 1 for fully paid and 0 for charged off
df['loan_repaid'] = df['loan_status'].map({'Fully Paid':1,'Charged Off':0})

# missing data percentage per category
print(100* df.isnull().sum()/len(df))

#revol_util and the pub_rec_bankruptcies have missing data points, 
#but they account for less than 0.5% of the total data. Let's drop them
df = df.drop('revol_util',axis=1)
df = df.drop('pub_rec_bankruptcies',axis=1)


#evaluating categories with missing data
print('unique job titles: ', df['emp_title'].nunique())
print(df['emp_title'].value_counts())

#considering that there is too many job titles to categorize let's drop this category
df = df.drop('emp_title',axis=1)

#'issue_d' column is not useful for us as there might be data leakage. Let's drop it
df = df.drop('issue_d',axis=1)

#evaluating debts according to worrking experience
emp_length_order = ['< 1 year','1 year','2 years','3 years','4 years','5 years',
					'6 years','7 years','8 years','9 years','10+ years']
plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order=emp_length_order,hue='loan_status')
plt.show()

charged_off = df[df['loan_status']=="Charged Off"].groupby("emp_length").count()['loan_status']
paid = df[df['loan_status']=="Fully Paid"].groupby("emp_length").count()['loan_status']
emp_len = charged_off/paid
#percentage of charged off per category is more or less the same, so let;s drop it
emp_len.plot(kind='bar')
plt.show()
df = df.drop('emp_length',axis=1)
df = df.drop('loan_status',axis=1) #not necessary anymore


#Evaluating 'title' and 'purpose' column
print(df['title'].head(10))
print(df['purpose'].head(10))

#they are the same, so let's drop 'title' column
df = df.drop('title',axis=1)


#Evaluating the last column: 'mort_acc'. Looking for correlation
print(df.corr()['mort_acc'].sort_values())
#correlates the most with total_acc column. Let's fill missing data with average mort_acc value
#for the corresponding total_acc value for that row.
total_acc_avg = df.groupby('total_acc').mean()['mort_acc']
def fill_mort_acc(total_acc,mort_acc):
	if np.isnan(mort_acc):
		return total_acc_avg[total_acc]
	else:
		return mort_acc

df['mort_acc'] = df.apply(lambda x: fill_mort_acc(x['total_acc'], x['mort_acc']), axis=1)


#Use next line to see string columns
#df.select_dtypes(['object']).columns


#converting string 'term' column into integer values
df['term'] = df['term'].apply(lambda term: int(term[:3]))

#dropping 'grade column' as duplicating 'subgrade' column
df = df.drop('grade',axis=1)

#getting dummies 

subgrade_dummies = pd.get_dummies(df['sub_grade'],drop_first=True)
df = pd.concat([df.drop('sub_grade',axis=1),subgrade_dummies],axis=1)
dummies = pd.get_dummies(df[['verification_status', 'application_type','initial_list_status','purpose' ]],drop_first=True)
df = df.drop(['verification_status', 'application_type','initial_list_status','purpose'],axis=1)
df = pd.concat([df,dummies],axis=1)

#as can be seen with df['home_ownership'].value_counts() 'home_ownership' has NONE and ANY columns,
#which needs to be labled as 'OTHER' to reduce categories count 
df['home_ownership']=df['home_ownership'].replace(['NONE', 'ANY'], 'OTHER')
dummies = pd.get_dummies(df['home_ownership'],drop_first=True)
df = df.drop('home_ownership',axis=1)
df = pd.concat([df,dummies],axis=1)


#Address is too copmlicated, so extracting ZIP code and replacing 'address' column
df['zip_code'] = df['address'].apply(lambda address:address[-5:])
dummies = pd.get_dummies(df['zip_code'],drop_first=True)
df = df.drop(['zip_code','address'],axis=1)
df = pd.concat([df,dummies],axis=1)

#getting year values from 'earliest_cr_year' column
df['earliest_cr_year'] = df['earliest_cr_line'].apply(lambda date:int(date[-4:]))
df = df.drop('earliest_cr_line',axis=1)



#splitting results from input data

X = df.drop('loan_repaid',axis=1).values
y = df['loan_repaid'].values

#performing test/training splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

#normalizing data

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)



############################
#NEURAL NETWORK CONSTRUCTION
############################

model = Sequential()

model.add(Dense(78,  activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(39, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(19, activation='relu'))
model.add(Dropout(0.2))
#output
model.add(Dense(units=1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam')

#fitting the model

model.fit(x=X_train, y=y_train, epochs=25, batch_size=256, validation_data=(X_test, y_test))

#Showing losses for evaluation
losses = pd.DataFrame(model.history.history)
losses[['loss','val_loss']].plot()
plt.show()


#creating a new random customer for testing 
random_customer = random.randint(0,len(df))
new_customer = df.drop('loan_repaid',axis=1).iloc[random_customer]
print('New random customer:', new_customer)

prediction = model.predict_classes(new_customer.values.reshape(1,76))
print('Predicted repayment is: ', prediction)
actual_repayment = df.iloc[random_customer]['loan_repaid']
print('Actual repayment is: ', actual_repayment)
