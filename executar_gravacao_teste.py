# pip install opencv-python
# pip install schedule

import time
from datetime import datetime, date
import cv2
import schedule

# globais para controlar o estado da gravação
filmagem = None
gravacao = None
gravando = False

def exibir_mensagem(mensagem):
    print(f"{datetime.now()}: {mensagem}")

def iniciar_gravacao():
    global filmagem, gravacao, gravando

    if not gravando:
        try:
            filmagem = cv2.VideoCapture(0)
            if not filmagem.isOpened():
                raise Exception("Não foi possível abrir a câmera!")

            w = int(filmagem.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(filmagem.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(filmagem.get(cv2.CAP_PROP_FPS))

            # Nome do arquivo 
            dataHora = datetime.now()
            dia = dataHora.strftime("%d_%m")
            hora = dataHora.strftime("%H_%M")
            nome_mp4 = f"gravacao{dia}_{hora}.mp4"

            gravacao = cv2.VideoWriter(nome_mp4, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

            # Gravação iniciada
            gravando = True
            exibir_mensagem("Início da Gravação")
        except Exception as e:
            exibir_mensagem(f"Erro ao iniciar a gravação: {e}")

def parar_gravacao():

    global filmagem, gravacao, gravando

    if gravando:
        exibir_mensagem("Finalizando a gravação...")

        if filmagem:
            filmagem.release()
        if gravacao:
            gravacao.release()
            cv2.destroyAllWindows()

        # Gravação finalizada
        gravando = False
        filmagem = None
        gravacao = None
        exibir_mensagem("Gravação finalizada")

    # Se não estiver gravando, não faz nada.

def agendar_gravacao():
    # Teste Horario 1
    schedule.every().day.at("14:00").do(iniciar_gravacao)
    schedule.every().day.at("14:02").do(parar_gravacao)
    # Teste Horario 2
    schedule.every().day.at("14:05").do(iniciar_gravacao)
    schedule.every().day.at("14:08").do(parar_gravacao)
    # Teste Horario 3
    schedule.every().day.at("14:10").do(iniciar_gravacao)
    schedule.every().day.at("14:12").do(parar_gravacao)

if __name__ == "__main__":
    agendar_gravacao()

    while True:
        schedule.run_pending()

        if gravando and filmagem is not None:
            success, frame = filmagem.read()
            if success:
                gravacao.write(frame)
        
        time.sleep(1)


