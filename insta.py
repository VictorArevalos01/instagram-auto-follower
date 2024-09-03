from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define a função para ler e listar o conteúdo do arquivo
def ler_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            if not conteudo:  # Verifica se o arquivo está vazio
                print("O arquivo está vazio.")
                return []
            return conteudo
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return []

def cria_lista_perfis():
    # Substitua 'seuarquivo.txt' pelo caminho do seu arquivo
    caminho = 'contas.txt'
    conteudo = ler_arquivo(caminho)

    # Verifica se o conteúdo foi retornado corretamente
    if conteudo:
        # Divide o conteúdo e limpa os itens
        lista = [item.strip() for item in conteudo.split("@") if item.strip()]
        return lista
    else:
        print("Não foi possível processar o arquivo.")

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Inicializa o WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abre o Instagram
driver.get('https://www.instagram.com')

# Espera a página carregar
time.sleep(1)

# Encontrar e clicar no botão de aceitar cookies (se houver)
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar')]"))
    )
    cookie_button.click()
except Exception as e:
    print("Botão de cookies não encontrado:", e)

# Fazer login - Substitua 'seu_usuario' e 'sua_senha' pelas suas credenciais
username = 'sua conta'
password = 'senha'

# Localiza o campo de nome de usuário e senha
user_field = driver.find_element(By.NAME, 'username')
pass_field = driver.find_element(By.NAME, 'password')

# Insere as credenciais e faz login
user_field.send_keys(username)
pass_field.send_keys(password)
pass_field.send_keys(Keys.RETURN)

# Espera o login ser processado
time.sleep(1)
perfils = cria_lista_perfis()

for perfil in perfils:
    # Procura o campo de pesquisa e pesquisa pelo usuário
    try:
        # Clica no <span> que contém "Pesquisa"
        search_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Pesquisa')]"))
        )
        search_span.click()

        # Aguarda o campo de pesquisa ficar visível e interagível
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )

        search_box.send_keys(perfil)
        time.sleep(1)  # Aguarde para os resultados aparecerem
        search_box.send_keys(Keys.RETURN)
        search_box.send_keys(Keys.RETURN)  # Pressione Enter novamente para confirmar


        search_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{perfil}')]"))
        )
        search_profile.click()

        # Aguarda o perfil ser carregado e clicar no botão "Seguir"
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='_ap3a _aaco _aacw _aad6 _aade']"))
        )
        follow_button.click()
        time.sleep(1)
    except Exception as e:
        print("Erro ao localizar ou interagir com o botão de seguir:", e)


time.sleep(1)

# Fecha o navegador
driver.quit()
