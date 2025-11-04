from functions.convertMsToDate import timeConvert


class Employee:
    def __init__(self , name , horaEntrada , horaSaida , setor , idMatricula , idTangerino):
        self.name = name
        self.horaEntrada_ms = horaEntrada
        self.horaSaida_ms = horaSaida
        self.setor = setor
        self.idMatricula = idMatricula
        self.idTangerino = idTangerino

    def minutos(self):
        if self.horaSaida_ms == None:
            return 0
        return (self.horaSaida_ms - self.horaEntrada_ms) / (1000 * 60)
    
    def ConverterData(self):
        response = {}
        if self.horaSaida_ms != None:
            response["dataSaida"] = timeConvert(self.horaSaida_ms)
        if self.horaEntrada_ms != None:
            response["dataEntrada"] = timeConvert(self.horaEntrada_ms)
        return response

    def DateTime_Entrada(self):
        if self.horaEntrada_ms == None: return None
        return timeConvert(self.horaEntrada_ms)
    
    def DateTime_Saida(self):
        if self.horaSaida_ms == None: return None
        return timeConvert(self.horaSaida_ms)