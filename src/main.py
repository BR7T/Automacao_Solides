from datetime import datetime , timedelta
import time
from functions.database import RecalcJornadaDatabase, addPunch
from functions.Employee import Employee
from functions.Solides.get import GetAllSolidesPontos , _GetAllEmployeesAndWorkPlace_

print("Iniciando")

def AtualizaBanco(obj):
    func = Employee(
        horaEntrada= obj.get("dateIn"),
        horaSaida= obj.get("dateOut"),
        idMatricula= obj.get("employeeExternalId"),
        idTangerino= obj.get("employeeId"),
        setor= obj.get("workPlaceName"),
        name= obj.get("employeeName")
    )
    if func.DateTime_Entrada() != None:
        addPunch(func.DateTime_Entrada() , func.idTangerino , tipo="1")

    print(func.DateTime_Saida())
    if func.DateTime_Saida() != None:
        addPunch(func.DateTime_Saida() , func.idTangerino , tipo="0")
        RecalcJornadaDatabase(func)

# altere a quantidade de dias retroativos aqui
diaconsulta = datetime.now().date() - timedelta(days=1)
dt = datetime.combine(diaconsulta, datetime.min.time())
form = int(dt.timestamp() * 1000)


inicio = time.time()
dataEmployees , dataWorkPlace = _GetAllEmployeesAndWorkPlace_()
fim = time.time()

print(f"Tempo para pegar informações de funcionário e local de trabalho: {fim - inicio:.4f}s")

baseWorkPlace = {w.get("id"): w.get("name")  for w in dataWorkPlace.get("content")}

baseEmployees = {}

inicio = time.time()
for e in dataEmployees['content']:
    w1 = e.get("workplaceList") or []
    wpl = w1[0].get("id") if w1 else None
    baseEmployees[e["id"]] = {
        "workPlaceId" : wpl,
        "workplaceName" : baseWorkPlace.get(wpl , "Desconhecido")
    }
fim = time.time()
print(f"Tempo para finalizar employees: {fim-inicio:.4f} segundos")


inicio = time.time()
page = 0
while True:
    resp = GetAllSolidesPontos(page , form)
    content = (resp or {}).get("content") or []

    if not content:
        break

    for obj in content:
        baseCruza = baseEmployees.get(obj.get("employeeId"))
        obj["workPlaceName"] = baseCruza.get("workplaceName")

        if obj.get("allowance"):
            continue
        AtualizaBanco(obj)
    print("finish a page")
    page += 1

fim = time.time()
print(f"Tempo para finalizar insert de tudo: {fim-inicio:.4f} segundos")