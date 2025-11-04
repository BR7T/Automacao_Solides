from datetime import timedelta
from functions import Employee
from .connection import connection


def ExistPunch(idTangerino, datePunch) -> bool | None:
    conn = connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT * FROM pontos WHERE id_tangerino = ?  AND datahora_ponto = ?
        """
        cursor.execute(query , (idTangerino , datePunch))
        result = cursor.fetchall()

        if len(result) == 0:
            return False
        else:
            return True
        
    except Exception as e:
        return None

def addPunch(ponto , idTangerino , tipo)->bool | None:
    if not ponto or not idTangerino:return
    conn = connection()
    cursor = conn.cursor()

    # verifica se ponto já existe, se já existir apenas passa para o próximo
    if ExistPunch(idTangerino=idTangerino , datePunch=ponto):
        print(f"Já existe, {idTangerino} , {ponto}")
        return None
    
    # adiciona ponto depois de verificado
    query = """
        INSERT INTO 
        pontos (id_tangerino , datahora_ponto , tipo)
        VALUES (? , ? , ?)
    """

    try:
        cursor.execute(query , (idTangerino , ponto , tipo))
        conn.commit()
        print("✅ adicionado com sucesso")
        return True
    except Exception as e:
        print(f"Erro ao adicionar ponto: {e}")
        return False
    

def RecalcJornadaDatabase(func : Employee):
    # define variáveis, dia que está sendo buscado e id tangerino
    conn = connection()
    cursor = conn.cursor()

    try:
        id_tangerino = func.idTangerino
        data = func.DateTime_Entrada().date()

        # procura todos os pontos no dia do usuário pelo id_tangerino
        query = "SELECT * FROM pontos WHERE id_tangerino = ? AND CAST(datahora_ponto as date) = ?"
        cursor.execute(query , (id_tangerino , data))
        result = cursor.fetchall()
        if len(result) > 1:
            print("começando a calcular")

            # usa função para calcular
            min = calcula_tempo_trabalhado(result)
            
            resultJornada = insertJornada_database(func , min)

            if resultJornada:
                print("✅ Jornada Adicionada com sucesso")
            elif resultJornada == False:
                print("❌ Falha ao adiconar Jornada")

    except Exception as e:
        print("Erro ao (re)calcular jornada: ", e)
        return False
    finally:
        cursor.close()
        conn.close()

    

def calcula_tempo_trabalhado(pontos):
    pontos.sort(key=lambda x : x[1])
    totalMinutos = timedelta()
    entrada = None

    for _ , datahora , tipo in pontos:
        if tipo == 1:
            entrada = datahora
        elif tipo == 0 and entrada:
            totalMinutos += datahora - entrada
            entrada = None

    return totalMinutos.total_seconds() / 60


def insertJornada_database(func:Employee , minutosTrabalhados):
    data = func.DateTime_Entrada().date()
    id_tangerino = func.idTangerino

    conn = connection()
    cursor = conn.cursor()
    try:
        resultExist = verifyJornada_database(dataJornada=data , id_tangerino=id_tangerino)

        if resultExist:
            query = """
                UPDATE jornada SET minutosTrabalhados =  ?
                WHERE id_tangerino = ? AND dataJornada = ?
            """
            cursor.execute(query , (minutosTrabalhados , id_tangerino , data))
            conn.commit()

            print("🔄️ Atualizado com sucesso")
            return True
        
        elif not resultExist:
            n_matricula = func.idMatricula
            setor = func.setor
            name = func.name

            query = """
                INSERT INTO jornada 
                (dataJornada , n_matricula , minutosTrabalhados , nome , id_tangerino , setor)
                VALUES
                (?,?,?,?,?,?)
            """
            cursor.execute(query , (data , n_matricula , minutosTrabalhados , name , id_tangerino , setor))

            conn.commit()
            print("✅ Inserido com sucesso - Jornada")
            return True

    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()


def verifyJornada_database(dataJornada, id_tangerino):
    print()
    #verifica se já existe a jornada no banco
    query = """
        SELECT 1 FROM jornada WHERE id_tangerino = ? AND datajornada = ?
    """
    conn = connection()
    cursor = conn.cursor()
    try:
        print()
        cursor.execute(query , (id_tangerino , dataJornada))

        return cursor.fetchone() is not None

    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()
