from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'TU_TOKEN_VERIFICACION'
PAGE_ACCESS_TOKEN = 'EAAID13bJC8sBOZCAJ0jgfXdF6vRwTZBs5yNP5WLcFAH8Ad0ZAMG16oRKZCeQtM6ZB371hZCcsb8uIT2Q5EfF5si56SAWePBUAq7q7uZClYtdfeorhkfsmO0w9CZC8XpsRMc7H3rJTe8Wxgc21t3NhY9fSvQAbEuFJi1CJCm0qmZC2FJAcaM8Fy9Y9Q61xWhU1myrZCwgZDZD'


def enviar_mensaje(recipient_id, mensaje):
    url = 'https://graph.facebook.com/v17.0/me/messages'
    params = {'access_token': PAGE_ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': mensaje}
    }
    requests.post(url, params=params, headers=headers, json=data)


@app.route('/webhook', methods=['GET'])
def verificar():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return challenge
    return 'Token inválido', 403


@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    data = request.json
    for entry in data['entry']:
        for mensaje_evento in entry['messaging']:
            if 'message' in mensaje_evento and 'text' in mensaje_evento['message']:
                texto = mensaje_evento['message']['text'].lower()
                sender_id = mensaje_evento['sender']['id']
                manejar_respuesta(sender_id, texto)
    return 'ok', 200


def manejar_respuesta(sender_id, texto):
    # Mensaje inicial
    if 'hola' in texto or 'información' in texto:
        enviar_mensaje(sender_id,
                       "¡Hola! Gracias por escribirnos. Soy parte del equipo de TEA KIDS. ¿Cuántos años tiene tu hijo y si tiene diagnóstico o ha asistido a escuela o terapia?")

    elif '2' in texto or 'menor de 3' in texto:
        enviar_mensaje(sender_id,
                       "A esta edad es clave trabajar comunicación e interacción antes de lo académico. ¿Te gustaría saber cómo ayudamos a niños pequeños?")

    elif '3' in texto or '4' in texto or '5' in texto or '6' in texto:
        enviar_mensaje(sender_id,
                       "Aquí trabajamos con un plan personalizado que mejora el lenguaje, socialización y autonomía. ¿Hay alguna área que te preocupe en específico?")

    elif 'lenguaje' in texto:
        enviar_mensaje(sender_id,
                       "Entiendo, la comunicación es una de las áreas que más preocupa a los padres. En TEA KIDS utilizamos estrategias como PECS y técnicas de imitación para que los niños aprendan a comunicarse de manera funcional. Trabajamos esto tanto en el aula como con los papás para reforzarlo en casa.")

    elif 'socialización' in texto:
        enviar_mensaje(sender_id,
                       "La socialización puede ser difícil para niños con TEA. Creamos actividades que fomentan la interacción en pequeños grupos, con guía personalizada y refuerzos positivos.")

    elif 'autonomía' in texto:
        enviar_mensaje(sender_id,
                       "Enseñamos rutinas como vestirse, comer, ir al baño, y seguir instrucciones, adaptadas al nivel del niño. Todo en un entorno que promueve seguridad y confianza.")

    elif 'qué es tea kids' in texto or 'qué hacen' in texto:
        enviar_mensaje(sender_id,
                       "En TEA KIDS preparamos a los niños con TEA para su vida escolar y social, con estrategias científicamente probadas y planificación individual. ¿Te gustaría saber más?")

    elif 'beneficios' in texto:
        enviar_mensaje(sender_id,
                       "✅ Aulas sin sobrecarga sensorial\n✅ Grupos pequeños (4 niños por terapeuta)\n✅ ABA, TEACCH, SAAC\n✅ Trabajo conjunto con padres. ¿Te gustaría conocer horarios y modalidad?")

    elif 'horario' in texto or 'modalidad' in texto:
        enviar_mensaje(sender_id,
                       "📅 Iniciamos el 11 de agosto\n⏰ Horarios: 8:30-11:30 y 12:00-3:00\n📍 Lunes a viernes con fase de adaptación. ¿Quieres más info o inscribir a tu hij@?")

    elif 'precio' in texto or 'cuánto cuesta' in texto:
        enviar_mensaje(sender_id,
                       "El costo es de $1,950 MXN por semana e incluye clases, reportes de avance y talleres para papás. Si te inscribes antes del 31 de julio, la inscripción es gratis. ¿Te gustaría agendar una visita?")

    elif 'visita' in texto:
        enviar_mensaje(sender_id,
                       "Nos encantaría que conozcas el lugar 😊 📍 Dirección: [DIRECCIÓN] ¿Qué día podríamos agendar tu visita?")

    else:
        enviar_mensaje(sender_id,
                       "Gracias por tu mensaje 😊 Estoy aquí para ayudarte. ¿Te gustaría saber cómo trabajamos con niños con autismo?")


# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)

