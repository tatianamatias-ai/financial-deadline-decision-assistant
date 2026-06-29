## Portuguese Version
##This project was originally developed in Portuguese as part of a real-world operational process in Brazil.

## BB Payment Deadline Assistant 
## Python application developed to automate financial payment deadline calculations,
## reducing operational risks and supporting decision-making processes.

from datetime import datetime, timedelta, time

def proximo_dia_util(data):
    proximo = data + timedelta(days=1)
    while proximo.weekday() >= 5: # 5=Sábado, 6=Domingo
        proximo += timedelta(days=1)
    return proximo

def anterior_dia_util(data):
    anterior = data - timedelta(days=1)
    while anterior.weekday() >= 5:
        anterior -= timedelta(days=1)
    return anterior

def formatar_dia_amigavel(data_alvo, hoje):
    if data_alvo == hoje:
        return "hoje"
    elif data_alvo == proximo_dia_util(hoje):
        return "amanhã"
    else:
        dias_semana = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
        return f"na {dias_semana[data_alvo.weekday()]} ({data_alvo.strftime('%d/%m')})"

def calcular_prazo_bb():
    print("\n" + "="*50)
    print("      SISTEMA DE MONITORAMENTO DE PRAZOS BB")
    print("="*50)
    
    # 1. Inputs com tratamento de erro
    tipo = input("Tipo de pagamento (1 para Benefício, 2 para Pecúlio): ").strip()
    tipo_nome = "Benefício" if tipo == "1" else "Pecúlio"
    
    data_str = input("Data da assinatura da OP (DD/MM/AAAA) [Enter para HOJE]: ").strip()
    if not data_str:
        data_assinatura = datetime.now().date()
    else:
        data_assinatura = datetime.strptime(data_str, "%d/%m/%Y").date()

    hora_str = input("Hora da assinatura da OP (HH:MM): ").strip()
    hora_assinatura = datetime.strptime(hora_str, "%H:%M").time()
    
    agora = datetime.now()
    hoje = agora.date()

    # 2. Quando o dinheiro cai na conta? (Regra: Até 14h D+1, após 14h D+2)
    if hora_assinatura <= time(14, 0):
        data_disponibilidade = proximo_dia_util(data_assinatura)
    else:
        data_disponibilidade = proximo_dia_util(proximo_dia_util(data_assinatura))

    # 3. Quando enviar o arquivo TXT e qual a hora limite?
    if tipo == "1": # Benefício
        data_envio = anterior_dia_util(data_disponibilidade)
        hora_limite_t = time(16, 0)
        justificativa_regra = "Benefício manda um dia antes do dinheiro estar em conta"
    else: # Pecúlio
        data_envio = data_disponibilidade
        hora_limite_t = time(16, 30)
        justificativa_regra = "Pecúlio manda no dia que o dinheiro já está na conta"

    # Criar o objeto datetime completo do prazo final para comparação
    prazo_final_dt = datetime.combine(data_envio, hora_limite_t)
    
    # 4. Lógica de Alertas de Tempo Real
    quando_enviar_texto = formatar_dia_amigavel(data_envio, hoje).upper()
    quando_dinheiro_cai = formatar_dia_amigavel(data_disponibilidade, hoje)
    
    print("\n" + "-"*50)
    
    # Caso 1: Prazo já encerrou
    if agora > prazo_final_dt:
        print(f"🔴 RESULTADO: Prazo de envio ENCERRADO em {data_envio.strftime('%d/%m/%Y')} às {hora_limite_t.strftime('%H:%M')} horas.")
    
    # Caso 2: Envie AGORA (Falta menos de 1 hora)
    elif data_envio == hoje and (prazo_final_dt - agora) <= timedelta(hours=1):
        minutos_faltantes = int((prazo_final_dt - agora).total_seconds() / 60)
        print(f"⚠️ RESULTADO: ENVIE AGORA! Faltam apenas {minutos_faltantes} minutos para encerrar a janela de envio.")
    
    # Caso 3: Envie Hoje/Amanhã (Dentro do prazo)
    else:
        print(f"🟢 RESULTADO: Envie {quando_enviar_texto} até as {hora_limite_t.strftime('%H:%M')}h.")

    print(f"\nJustificativa: {justificativa_regra} e o dinheiro estará na conta {quando_dinheiro_cai}.")
    print("="*50 + "\n")

if __name__ == "__main__":
    calcular_prazo_bb()

    