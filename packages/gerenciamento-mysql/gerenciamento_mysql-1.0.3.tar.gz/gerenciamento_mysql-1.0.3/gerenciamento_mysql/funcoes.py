import mysql.connector
from datetime import datetime 

host_name = ""
user_name = ""
password_name = ""
database_name = ""
conexao = ""
cursor = ""

def conectar(host_i:str,user_i:str,password_i:str,database_i:str):
    global host_name
    global user_name
    global password_name
    global database_name
    global cursor
    global conexao

    host_name = host_i
    user_name = user_i
    password_name = password_i
    database_name = database_i

    conexao = mysql.connector.connect(
    host= host_name,    
    user= user_name,
    password= password_name,
    database= database_name
    )
    cursor = conexao.cursor()



# Funções Internas

# Verifica se o email já esta sendo utilizado
def src_verificarUsoEmail(tabela:str, email:str):
    conexao.commit()

    comando = f'SELECT * FROM {tabela} WHERE email = "{email}"'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    if ((len(resultado)) != 0):
        return True
    else:
        return False
    

# Retorna a hora atual:
def src_RetornoHora():
    hora_atual = datetime.now()
    hora_atual = hora_atual.time()
    hora_atual = str(hora_atual)

    return hora_atual[0:8]


# Retorna a data atual:
def src_RetornoData():
    data_atual = datetime.now()
    data_atual = data_atual.date()
    data_atual = data_atual.strftime("%Y-%m-%d")

    return data_atual


# Retorna o id do usuario:
def src_RetornoIdUsuario(tabela:str, campoId:str, campoEmail:str, valorEmail:str):
    conexao.commit()

    comando = f'SELECT {campoId} FROM {tabela} WHERE {campoEmail} = "{valorEmail}"'
    cursor.execute(comando)
    id_usuario = cursor.fetchall()
    id_usuario = id_usuario[0][0]

    return int(id_usuario)

  
# Verifica a validade do email:
def src_verificarValidadeEmail(email:str):
  if '@' in email and '.' in email:
    return True
  else:
    return False
  


# Funções Externas

# Cria uma conta com nome, email e senha:
def criarConta(tabela:str, campoNome:str, campoEmail:str, campoSenha:str, valorNome:str, valorEmail:str, valorSenha:str):
    try: 
        emailUtilizado = src_verificarUsoEmail(tabela,valorEmail)

        if (emailUtilizado == True):
            return [False, 'Email Utilizado']
        
        else:
            emailValido = src_verificarValidadeEmail(valorEmail)

            if (emailValido == True):
                comando = f'INSERT INTO {tabela} ({campoNome},{campoEmail},{campoSenha}) VALUES("{valorNome}","{valorEmail}","{valorSenha}")'
                cursor.execute(comando)
                conexao.commit()

            else:
                return [False, 'Insira um email válido']
            
    except:
        return [False, 'Erro ao tentar executar a função']


# Faz login em uma conta utilizando email e senha:
def logarConta(tabela:str, campoEmail:str, campoSenha:str, valorEmail:str, valorSenha:str):
    try:
        conexao.commit()

        comando = f'SELECT * FROM {tabela} WHERE {campoEmail}="{valorEmail}" AND {campoSenha}="{valorSenha}"'
        cursor.execute(comando)
        resultado = cursor.fetchall()

        if ((len(resultado)) !=0):
            return True
        else:
            return [False, 'Conta não encontrada']
    except:
        return [False, 'Erro ao tentar executar a função']
    

# Cria um log com: id do usuario que fez o log, motivo do log, data, hora
def registrarLog(tabelaLOG:str, tabelaUsuario:str, campoIdLog:str, campoMotivoLog, campoDataLog:str, campoHoraLog:str, campoIdUsuario:str, campoEmail:str, valorEmail:str, motivoLog:str):
    try:
        conexao.commit()

        data = src_RetornoData()
        hora = src_RetornoHora()
        id = src_RetornoIdUsuario(tabelaUsuario,campoIdUsuario,campoEmail,valorEmail)

        comando = f'INSERT INTO {tabelaLOG} ({campoIdLog},{campoMotivoLog},{campoDataLog},{campoHoraLog}) VALUES("{id}","{motivoLog}","{data}","{hora}")'
        cursor.execute(comando)
        conexao.commit()

        return True
    except:
        return [False, 'Erro ao executar a função']