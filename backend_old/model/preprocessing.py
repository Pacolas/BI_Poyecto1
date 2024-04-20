
import inflect
import nltk
import re
from pattern.es import parse
from nltk.corpus import stopwords
import unicodedata
from nltk.stem import  WordNetLemmatizer, SnowballStemmer
from sklearn.base import BaseEstimator, TransformerMixin
class DataFrameColumnTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X['Review'] = X['Review'].apply(remove_non_ascii)
        X['Review'] = X['Review'].apply(limpiar_texto)
        X['Review'] = X['Review'].apply(expandir_contracciones)
        X['Review'] = X['Review'].apply(filter_substrings)
        X['Review'] = X['Review'].apply(eliminar_stopwords)
        X['Review'] = X['Review'].apply(eliminar_risas)
        return X


p = inflect.engine()
stopwords_es = set(stopwords.words('spanish'))
contracciones = {
    "hotel": "",
    "si": "",
    "nacionál": "",
    "naciones": "",
    "útlimo": "nuestro",
    "si": "si",
    "tengo": "yo tengo",
    "tu": "tu",
    "tus": "tu",
    "un": "uno",
    "calidad": "cali",
    "excelent": "excelente",
    'experient': 'experiencia',
    'tom': '',
    'hor': 'horrible',
    'aqui': '',
    'aquí':'',
    'no':'negacion',
    'lugar': 'sitio',
    'establecimiento':'sitio'

}
substrings_to_remove = ['aloj']

def remove_non_ascii(texto):
    """Remove non-ASCII characters from a string"""
    new_texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_texto
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-zA-Záéíóúüñ\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)

    return texto

def expandir_contracciones(texto):
    palabras = texto.split()
    palabras_expandidas = [contracciones.get(palabra, palabra) for palabra in palabras]
    texto_expandido = ' '.join(palabras_expandidas)
    return texto_expandido

def filter_substrings(texto):
    expanded_document = expandir_contracciones(texto)
    filtered_document = []
    for word in expanded_document.split():
        is_substring = any(substring in word for substring in substrings_to_remove)
        if not is_substring:
            filtered_document.append(word)
    filtered_texto = " ".join(filtered_document)
    return filtered_texto


def eliminar_stopwords(texto):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stopwords_es]
    texto_filtrado = ' '.join(palabras_filtradas)
    return texto_filtrado


def eliminar_risas(texto):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if "jaj" not in stopwords_es]
    texto_filtrado = ' '.join(palabras_filtradas)
    return texto_filtrado

def tokenize_spanish(text):
    parsed_text = parse(text, tokenize=True, tags=False, chunks=False)
    tokens = [token[0] for sentence in parsed_text.split() for token in sentence]
    return tokens

def preprocessing(data_t):
    download_nltk_resources()
    data_t['Review'] = data_t['Review'].apply(eliminar_risas)
    data_t['Review'] = data_t['Review'].apply(limpiar_texto)
    data_t['Review'] = data_t['Review'].apply(expandir_contracciones)
    data_t['Review'] = data_t['Review'].apply(eliminar_stopwords)
    data_t['Review'] = data_t['Review'].apply(filter_substrings)
    data_t['Review'] = data_t['Review'].apply(remove_non_ascii)
    validation(data_t)
    data_t['words'] = data_t['Review'].apply(tokenize_spanish)
    normalization(data_t)
    eliminar_ambiguedad(data_t)

def validation(data_t):
    data_t.dropna(inplace=True)
    data_t.drop_duplicates(inplace=True)

def stem_words(words, stemmer_es):
    """Stem words in list of tokenized words"""
    stems = [stemmer_es.stem(word) for word in words]
    
    return stems

def lemmatize_words(words,lemmatizer_es):
    """Lemmatize words in list of tokenized words"""
    lemmas = [lemmatizer_es.lemmatize(word) for word in words]
    return lemmas

def stem_and_lemmatize(words):
    stems = stem_words(words,  SnowballStemmer('spanish'))
    lemmas = lemmatize_words(words,  WordNetLemmatizer())

    return stems + lemmas

def normalization(data_t):
    data_t['words'] = data_t['words'].apply(stem_and_lemmatize)
    data_t['words'] = data_t['words'].apply(lambda x: ' '.join(map(str, x)))


def download_nltk_resources():
    
    nltk.download('wordnet')  
    nltk.download('omw')  
    nltk.download('punkt')
    nltk.download('stopwords')   
    
    


from collections import defaultdict

def eliminar_ambiguedad(data_t):
    palabras_a_eliminar_por_clase = {
    1: ['hermoso', 'herm','hermos','pront','pronto','pron', 'volver','volv', 'vol','volve','alto', 'q', 'unic','fri','zona','iba','pero','do','carr','habana', 'cambi','veces','recom','agrad','cosas','tom','internet','estrellas','problem','tres','siempre','dijo','dic', 'sal','encontr','malo','client', 'sucio','fin','viejo','gente','pedimos','hech','hace', 'quier','viej','vist','vista','amabl','experient','check','ver','señor','tan','día','bien', 'excelente', 'buena', 'mejor', 'si', 'dieron', 'así', 'mal', 'solo', 'pues', 'buen', 'buffet', 'tour', 'aunque','bueno','cuba','decir','despues','además','menos','pesim','normal','alrededor','general','ofrec','ofrece','decepcion', 'turist','turista', 'alrededor','casi','dijeron'],
    2: ['terribl','hoteles','vist','taxi','agua', 'agu','embargo', 'mes','pedimos','acondicion','acondicionado','humedad','embarg','noch','olor','bonit','gust','habana', 'igual','agrad','grand','bastant','mala','recomiendo','especial','pesim','recepcion','bien', 'excelente', 'buena', 'dieron', 'así', 'peor', 'buen', 'mejor', 'solo', 'buffet', 'tour', 'aunque','demasi', 'suci','sucio','pesimo','vista', 'bueno','mas','tan','cuba','tener','realmente','cuban', 'pm','mala','normal','hor','general','ofrec','ofrece','realmente','después','limpio','limpi','ningun','ademas','bueno','actitud','nunc','nunca','mayor'],
    3: ['terribles','terribl','jam','negacion','mojit','interes', 'vista', 'interesante', 'cen','playa','cam','do','monton','sent','lado','grande','gui','pena','montón', 'ciudad', 'problem', 'mayor', 'cuc','tener', 'cuent','amable','famili', 'sabor','dec', 'sitio','pes','pag','función', 'bueno','recom','dej', 'llegar', 'cad', 'cambi', 'allí','baj', 'alli', 'unic', 'cerca','gust','punt','cuba','pod', 'estanci','cub','cerc','quier','ma', 'men','comod','ahi','pase','histori','nuev','historia','cada','medi','mas','mar','ped','beb','precios','grand','segur','ofrec','much','parte','unas','principal','amabl','gust','cer','pues','acondicion','precios','verd','ten','reserv','así','dos','ir','habit','caro','especial','buen', 'buena', 'mejor', 'mala', 'muy', 'bien', 'mal', 'gran', 'cali', 'limpi', 'buffet', 'trat', 'excelent', 'demasiado', 'malecon', 'despues','disfrut','q','demasi','realmente','excelente','bonit', 'bonito','bonita','demasi','experient','dieron'],
    4: ['terribles','siti','terribl','jam','precio','precio','perdi','diner', 'mayor','tenido','perdida', 'dinero','negacion','unas', 'par', 'compr', 'ma', 'muse', 'grand','haban','etc','habit','general','aunqu','tiempo','personal','buffet','bastante','mal', 'mejor', 'peor','agradab', 'agradable', 'excelente', 'excelent', 'solo', 'esper', 'espera', 'esperar', 'aunque','mas','tan', 'realmente', 'increible', 'increi','much','increibl','estrellas','general','agra','ningun','ningun','general','maravill','maravilla','viej','realment','cada','así','encant', 'conoc', 'cub','principal','vieja','calor','hacer','final','hermos','encant','niñ','llen','antigu','hermos','increibl'],
    5: ['volveri','terribles','siti','terribl','jam','lug','falta','precio','precio','perdi','diner', 'mayor','tenido','perdida', 'dinero','otro','gusto','pero','negacion','comod', 'camin','hacer','dentro','malecon','dud','puedes','cada','ambientes','encontr','unas','bonit','bonita','com','personal','recep','recepcion','decente','do', 'agradab', 'agradable','buen', 'buena', 'reserv', 'bien', 'historia', 'solo', 'esper', 'espera', 'esperar', 'instal', 'viej', 'bogot', 'tan', 'dos', 'alli', 'aunque', 'bien', 'bueno','estrellas','general','problema', 'problem','agra','ningun','casi','habana']
    }
    for index, row in data_t.iterrows():
        words = row['words'].split()
        category = row['Class']
        palabras_a_eliminar = palabras_a_eliminar_por_clase.get(category, [])
        words = [word for word in words if word not in palabras_a_eliminar]
        data_t.at[index, 'words'] = ' '.join(words)

def predict_process(dataframe):

    dataframe['Review'] = dataframe['Review'].apply(limpiar_texto)
    dataframe['Review'] = dataframe['Review'].apply(expandir_contracciones)
    dataframe['Review'] = dataframe['Review'].apply(eliminar_stopwords)
    dataframe['Review'] = dataframe['Review'].apply(filter_substrings)
    dataframe['Review'] = dataframe['Review'].apply(remove_non_ascii)
    dataframe['words'] = dataframe['Review'].apply(tokenize_spanish)
    dataframe['words'].dropna()
    dataframe['words'] = dataframe['words'].apply(stem_and_lemmatize)
    dataframe['words'] = dataframe['words'].apply(lambda x: ' '.join(map(str, x)))
