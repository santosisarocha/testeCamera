import time
from datetime import datetime
import cv2
import schedule

# globais para controlar o estado da gravação
filmagem = None
gravacao = None
gravando = False
fps = 30  

def exibir_mensagem(mensagem):
    print(f"{datetime.now()}: {mensagem}")

def iniciar_gravacao():
    global filmagem, gravacao, gravando, fps

    if not gravando:
        try:
            filmagem = cv2.VideoCapture(0)
            if not filmagem.isOpened():
                raise Exception("Não foi possível abrir a câmera!")

            w = int(filmagem.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(filmagem.get(cv2.CAP_PROP_FRAME_HEIGHT))

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

def agendar_gravacao():
    schedule.every().day.at("15:05").do(iniciar_gravacao)
    schedule.every().day.at("15:07").do(parar_gravacao)
    schedule.every().day.at("14:05").do(iniciar_gravacao)
    schedule.every().day.at("14:08").do(parar_gravacao)
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
        

