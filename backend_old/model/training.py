import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
import numpy as np
from collections import defaultdict
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.base import BaseEstimator, ClassifierMixin
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import backend_old.model.preprocessing as prep
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(conf_matrix, classes, save_path=None):
    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()  # Cerrar el gráfico después de guardar

def train_model(data_t):
    prep.preprocessing(data_t)
    X_data, y_data = data_t['words'], data_t['Class']
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.3, random_state=1)
    
    model = vectorize_model(X_train, y_train)  # Retornamos también el vectorizador CountVectorizer

    y_pred = model.predict(X_test)
  
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Guardar el modelo entrenado
    joblib.dump(model, "./backend_old/model/ml_models/trained/"+ data_t['version'][0]+'.pkl')

    # Guardar matriz de confusión
    plot_confusion_matrix(conf_matrix, classes=np.unique(y_data), save_path="./backend_old/model/ml_models/mtz_confussion/confusion_matrix%s.png"%( data_t['version'][0]))
    # Utilizar las funciones para generar los wordclouds y guardarlos en el directorio especificado
    print("Creare nubes")
    generate_wordclouds_for_categories(data_t,data_t['version'][0] ,'./backend_old/model/ml_models/wordclouds/' )


    return createMetrics(accuracy, precision, recall, f1)

def vectorize_model(X_train, y_train):
    steps = [
        ('vectorizer', CountVectorizer()),  # Paso de extracción de características
        ('vector2', TfidfTransformer()),  
        ('model', SVC(kernel='linear', C=1)),  # Paso de modelo de clasificación
    ]
    pipeline = Pipeline(steps)
    pipeline.fit(X_train, y_train)
    return pipeline

def createMetrics(accuracy, precision, recall, f1):
    return {'accuracy:' : accuracy, 'precision': precision, 'recall': recall , 'f1': f1}   


def sqltoDF(sql_result):
    if len(sql_result) == 0:
        return pd.DataFrame()  # Si no hay resultados, devolver DataFrame vacío
    else:
        # Convertir los resultados en un DataFrame utilizando los nombres de columnas proporcionados
        columns = ["id", "Review", "Class", "version"]

        return pd.DataFrame(sql_result, columns=columns)






def generate_wordclouds_for_categories(data_t,version, save_path):
    word_counts_by_category = defaultdict(lambda: defaultdict(int))

    for index, row in data_t.iterrows():
        words = row['words'].split()
        category = row['Class']
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1
        for word, count in word_counts.items():
            word_counts_by_category[category][word] += count

    wordcloud = WordCloud(width=800, height=400, background_color='white')

    for category, word_counts in word_counts_by_category.items():
        cloud = wordcloud.generate_from_frequencies(word_counts)
        plt.figure(figsize=(10, 6))
        plt.imshow(cloud, interpolation='bilinear')
        plt.title(f'WordCloud para la categoría "{category}"')
        plt.axis('off')
        plt.savefig(f"{save_path}/WordCloud_{version}_{category}.png")
        plt.close()
 