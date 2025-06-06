import os
import pickle
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# --- Código de carregamento dos modelos aqui (como no seu código atual) ---
# Garanta que as variáveis:
# model_colesterol
# model_diabetes
# model_obesidade
# model_hipertensao
# estejam definidas (carregadas ou None) antes desta função.
# O código de carregamento dos modelos deve estar fora das funções de rota,
# tipicamente logo após a criação do 'app = Flask(__name__)'.

MODEL_PATH_Colesterol = 'modelo-colesterol.pkcls'
MODEL_PATH_Diabetes = 'modelo-diabetes.pkcls'
MODEL_PATH_Obesidade = 'modelo-obesidade.pkcls'
MODEL_PATH_Hipertensao = 'modelo-hipertesao.pkcls'

model_colesterol = None
model_diabetes = None
model_obesidade = None
model_hipertensao = None

# --- Carregar Modelo de Colesterol ---
try:
    if not os.path.exists(MODEL_PATH_Colesterol):
        print(f"ERRO: O arquivo do modelo '{MODEL_PATH_Colesterol}' (Colesterol) não foi encontrado.")
    else:
        with open(MODEL_PATH_Colesterol, 'rb') as file:
            model_colesterol = pickle.load(file)
        print(f"Modelo '{MODEL_PATH_Colesterol}' (Colesterol) carregado com sucesso!")
except Exception as e:
    print(f"ERRO ao carregar o modelo de Colesterol '{MODEL_PATH_Colesterol}': {e}")

# --- Carregar Modelo de Diabetes ---
try:
    if not os.path.exists(MODEL_PATH_Diabetes):
        print(f"ERRO: O arquivo do modelo '{MODEL_PATH_Diabetes}' (Diabetes) não foi encontrado.")
    else:
        with open(MODEL_PATH_Diabetes, 'rb') as file:
            model_diabetes = pickle.load(file)
        print(f"Modelo '{MODEL_PATH_Diabetes}' (Diabetes) carregado com sucesso!")
except Exception as e:
    print(f"ERRO ao carregar o modelo de Diabetes '{MODEL_PATH_Diabetes}': {e}")

# --- Carregar Modelo de Obesidade ---
try:
    if not os.path.exists(MODEL_PATH_Obesidade):
        print(f"ERRO: O arquivo do modelo '{MODEL_PATH_Obesidade}' (Obesidade) não foi encontrado.")
    else:
        with open(MODEL_PATH_Obesidade, 'rb') as file:
            model_obesidade = pickle.load(file)
        print(f"Modelo '{MODEL_PATH_Obesidade}' (Obesidade) carregado com sucesso!")
except Exception as e:
    print(f"ERRO ao carregar o modelo de Obesidade '{MODEL_PATH_Obesidade}': {e}")

# --- Carregar Modelo de Hipertensão ---
try:
    if not os.path.exists(MODEL_PATH_Hipertensao):
        print(f"ERRO: O arquivo do modelo '{MODEL_PATH_Hipertensao}' (Hipertensão) não foi encontrado.")
    else:
        with open(MODEL_PATH_Hipertensao, 'rb') as file:
            model_hipertensao = pickle.load(file)
        print(f"Modelo '{MODEL_PATH_Hipertensao}' (Hipertensão) carregado com sucesso!")
except Exception as e:
    print(f"ERRO ao carregar o modelo de Hipertensão '{MODEL_PATH_Hipertensao}': {e}")


@app.route('/')
def home():
    return render_template('index.html')

# Rota para predição - Recebe os dados do formulário
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Coletar e validar os dados do formulário
            age = int(request.form['idade']) # Idade como int
            height = float(request.form['altura'])
            weight = float(request.form['peso'])
            SBP = float(request.form['sbp'])
            DBP = float(request.form['dbp'])
            BLDS = float(request.form['blds'])
            tot_chole = float(request.form['colesterol'])

            # 2. Calcular o BMI
            if height > 0:
                height_m = height / 100.0 # Converte cm para metros
                BMI = weight / (height_m ** 2)
            else:
                return "Erro: Altura inválida. Por favor, insira um valor positivo.", 400 # Retorna erro para o usuário
            
            # --- 3. Criar um DataFrame único com todos os atributos capturados e calculados ---
            # Defina a ordem das colunas para este DataFrame central.
            # Esta ordem é para sua organização e debug.
            all_features_ordered = [
                'idade', 'altura', 'peso', 'BMI', 'sbp', 'dbp', 'blds', 'colesterol'
            ]
            
            # Crie um dicionário com os dados do usuário
            user_input_data = {
                'idade': age,
                'altura': height,
                'peso': weight,
                'BMI': BMI,
                'sbp': SBP,
                'dbp': DBP,
                'blds': BLDS,
                'colesterol': tot_chole
            }
            
            # Crie o DataFrame central com a ordem definida
            user_data = pd.DataFrame([user_input_data], columns=all_features_ordered)
            
            print("\nDataFrame de dados do usuário:")
            print(user_data)
            print("-" * 30)

            # --- 4. Preparar os dados para CADA modelo específico a partir de 'user_data' ---
            # CORREÇÃO PRINCIPAL: As listas de features agora contêm 8 features,
            # presumindo que seus modelos foram treinados com todas elas na mesma ordem.
            # AJUSTE AQUI SE SEUS MODELOS Orange3 USAM SUBSETS OU ORDEM DIFERENTE!

            # Para todos os modelos, vamos assumir que eles esperam as 8 features na mesma ordem
            # em que elas aparecem no 'user_data'.
            common_model_features = [
                'idade', 'altura', 'peso', 'BMI', 'sbp', 'dbp', 'blds', 'colesterol'
            ]

            data_colesterol = user_data[common_model_features]
            data_diabetes = user_data[common_model_features]
            data_obesidade = user_data[common_model_features]
            data_hipertensao = user_data[common_model_features]

            # --- 5. Fazer as predições ---
            # Inicializar resultados para cada modelo
            predicao_colesterol = "N/A"
            predicao_diabetes = "N/A"
            predicao_obesidade = "N/A"
            predicao_hipertensao = "N/A"

            if model_colesterol:
                try:
                    # Chame .predict() para obter a classe predita
                    predicao_colesterol = model_colesterol.predict(data_colesterol)[0]
                except Exception as e:
                    predicao_colesterol = f"Erro na predição do Colesterol: {e}"
                    print(f"Erro ao predizer colesterol: {e}")
            else:
                predicao_colesterol = "Modelo de Colesterol não carregado."
                print("Modelo de Colesterol não disponível para predição.")

            if model_diabetes:
                try:
                    predicao_diabetes = model_diabetes.predict(data_diabetes)[0]
                except Exception as e:
                    predicao_diabetes = f"Erro na predição da Diabetes: {e}"
                    print(f"Erro ao predizer diabetes: {e}")
            else:
                predicao_diabetes = "Modelo de Diabetes não carregado."
                print("Modelo de Diabetes não disponível para predição.")

            if model_obesidade:
                try:
                    predicao_obesidade = model_obesidade.predict(data_obesidade)[0]
                except Exception as e:
                    predicao_obesidade = f"Erro na predição da Obesidade: {e}"
                    print(f"Erro ao predizer obesidade: {e}")
            else:
                predicao_obesidade = "Modelo de Obesidade não carregado. (Verifique o erro de PyQt na inicialização!)"
                print("Modelo de Obesidade não disponível para predição.")
            
            if model_hipertensao:
                try:
                    predicao_hipertensao = model_hipertensao.predict(data_hipertensao)[0]
                except Exception as e:
                    predicao_hipertensao = f"Erro na predição da Hipertensão: {e}"
                    print(f"Erro ao predizer hipertensão: {e}")
            else:
                predicao_hipertensao = "Modelo de Hipertensão não carregado."
                print("Modelo de Hipertensão não disponível para predição.")

            # --- 6. Retornar os resultados para o usuário ---
            # O 'resultados.html' precisará ser criado na sua pasta 'templates'
            # e poderá acessar essas variáveis passadas.
            return render_template('resultados.html', 
                                   colesterol=predicao_colesterol,
                                   diabetes=predicao_diabetes,
                                   obesidade=predicao_obesidade,
                                   hipertensao=predicao_hipertensao,
                                   idade=age, altura=height_m, peso=weight, bmi=BMI,
                                   sbp=SBP, dbp=DBP, blds=BLDS, tot_chole=tot_chole)
            
        except KeyError as e:
            # Erro se algum campo esperado no request.form não foi encontrado
            print(f"Erro de KeyError: {e}")
            return f"Erro: Campo do formulário faltando. Por favor, preencha todos os campos. Detalhe: {e}", 400
        except ValueError:
            # Erro se o valor de um campo não puder ser convertido para float/int
            print(f"Erro de ValueError: {e}")
            return "Erro: Os valores de idade, peso, altura, etc., devem ser números válidos. Por favor, verifique sua entrada.", 400
        except Exception as e:
            # Captura qualquer outro erro inesperado no processo de predição
            print(f"Ocorreu um erro inesperado na função predict(): {e}")
            return f"Ocorreu um erro interno no servidor ao processar sua solicitação: {e}", 500

    else:
        # Se a rota for acessada por GET (e não por POST do formulário), redireciona para a home
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)