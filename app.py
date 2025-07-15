from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'paschoalotto_ai_companion_secret_key_2024'

# Language configuration
LANGUAGES = {
    'en': {
        'name': 'English',
        'flag': '🇺🇸'
    },
    'pt': {
        'name': 'Português',
        'flag': '🇧🇷'
    }
}

# Translations
TRANSLATIONS = {
    'en': {
        'app_title': 'Paschoalotto AI Companion',
        'app_subtitle': 'Intelligent Debt Collection Assistant',
        'dashboard': 'Dashboard',
        'live_call': 'Live Call',
        'performance': 'Performance',
        'training': 'Training',
        'settings': 'Settings',
        'welcome_message': 'Welcome to your AI Companion',
        'daily_goals': 'Daily Goals',
        'calls_made': 'Calls Made',
        'contacts_reached': 'Contacts Reached',
        'payments_collected': 'Payments Collected',
        'collection_amount': 'Collection Amount',
        'ai_suggestions': 'AI Suggestions',
        'customer_insights': 'Customer Insights',
        'compliance_alerts': 'Compliance Alerts',
        'start_call': 'Start Call',
        'end_call': 'End Call',
        'customer_said': 'What did the customer say?',
        'quick_responses': 'Quick Responses',
        'cant_pay': "Can't pay",
        'wants_discount': 'Wants discount',
        'angry': 'Angry',
        'interested': 'Interested',
        'needs_time': 'Needs time',
        'disputes_debt': 'Disputes debt',
        'ai_recommendations': 'AI Recommendations',
        'compliance': 'COMPLIANCE',
        'urgent': 'URGENT',
        'suggestion': 'SUGGESTION',
        'offer': 'OFFER',
        'insight': 'INSIGHT',
        'success_probability': 'Success Probability',
        'audio_controls': 'Audio Controls',
        'audio_alerts': 'Audio Alerts',
        'text_to_speech': 'Text to Speech',
        'volume': 'Volume',
        'use': 'Use',
        'modify': 'Modify',
        'copy': 'Copy',
        'analyze': 'Analyze',
        'click_and_speak': 'Click and Speak',
        'listening': 'Listening...',
        'speak_now': 'Speak now...',
        'voice_not_supported': 'Voice recognition not supported in this browser',
        'type_customer_message': 'Type or use buttons below...',
        'conversation_history': 'Conversation History',
        'demo_instructions': 'Demo Instructions',
        'how_to_test': 'How to Test the Enhanced Interface',
        'input_methods': 'Input Methods',
        'output_methods': 'Output Methods',
        'start_demo': 'Start Demo',
        'demo_started': 'Demo started! Test the input methods.',
        'demo_ended': 'Demo ended.',
        'voice_error': 'Voice recognition error',
        'text_copied': 'Text copied!',
        'recommendation_used': 'Recommendation used!',
        'enter_valid_message': 'Enter a valid customer message'
    },
    'pt': {
        'app_title': 'Paschoalotto AI Companion',
        'app_subtitle': 'Assistente Inteligente para Cobrança',
        'dashboard': 'Painel',
        'live_call': 'Chamada ao Vivo',
        'performance': 'Performance',
        'training': 'Treinamento',
        'settings': 'Configurações',
        'welcome_message': 'Bem-vindo ao seu AI Companion',
        'daily_goals': 'Metas Diárias',
        'calls_made': 'Chamadas Feitas',
        'contacts_reached': 'Contatos Alcançados',
        'payments_collected': 'Pagamentos Coletados',
        'collection_amount': 'Valor Coletado',
        'ai_suggestions': 'Sugestões do AI',
        'customer_insights': 'Insights do Cliente',
        'compliance_alerts': 'Alertas de Compliance',
        'start_call': 'Iniciar Chamada',
        'end_call': 'Encerrar Chamada',
        'customer_said': 'O que o cliente disse?',
        'quick_responses': 'Respostas Rápidas',
        'cant_pay': 'Não pode pagar',
        'wants_discount': 'Quer desconto',
        'angry': 'Está irritado',
        'interested': 'Interessado',
        'needs_time': 'Precisa de tempo',
        'disputes_debt': 'Contesta dívida',
        'ai_recommendations': 'Recomendações do AI',
        'compliance': 'COMPLIANCE',
        'urgent': 'URGENTE',
        'suggestion': 'SUGESTÃO',
        'offer': 'OFERTA',
        'insight': 'INSIGHT',
        'success_probability': 'Probabilidade de Sucesso',
        'audio_controls': 'Controles de Áudio',
        'audio_alerts': 'Alertas Sonoros',
        'text_to_speech': 'Texto para Fala',
        'volume': 'Volume',
        'use': 'Usar',
        'modify': 'Modificar',
        'copy': 'Copiar',
        'analyze': 'Analisar',
        'click_and_speak': 'Clique e Fale',
        'listening': 'Ouvindo...',
        'speak_now': 'Fale agora...',
        'voice_not_supported': 'Reconhecimento de voz não suportado neste navegador',
        'type_customer_message': 'Digite ou use os botões abaixo...',
        'conversation_history': 'Histórico da Conversa',
        'demo_instructions': 'Instruções da Demo',
        'how_to_test': 'Como Testar a Interface Aprimorada',
        'input_methods': 'Métodos de Entrada',
        'output_methods': 'Métodos de Saída',
        'start_demo': 'Iniciar Demo',
        'demo_started': 'Demo iniciada! Teste os métodos de entrada.',
        'demo_ended': 'Demo encerrada.',
        'voice_error': 'Erro no reconhecimento de voz',
        'text_copied': 'Texto copiado!',
        'recommendation_used': 'Recomendação utilizada!',
        'enter_valid_message': 'Digite uma mensagem válida do cliente'
    }
}

# AI Response Templates
AI_RESPONSES = {
    'en': {
        'cant_pay': {
            'compliance': "Don't mention legal action. Focus on payment solutions.",
            'suggestion': "I understand your situation. Let's find a solution that works for you. What amount could you pay monthly?",
            'offer': "Offer 6-month installments or 30% discount for immediate payment",
            'insight': "Customer in financial hardship. High probability of accepting installments (75%)",
            'probability': 75
        },
        'wants_discount': {
            'suggestion': "I can check what options we have available. For immediate payment, we can offer special conditions.",
            'offer': "Authorized discount up to 40% for immediate payment or 25% for payment in up to 3 installments",
            'insight': "Customer interested in negotiating. High probability of closing (85%)",
            'probability': 85
        },
        'angry': {
            'compliance': "Customer is angry. Maintain calm and empathetic tone. Don't argue.",
            'urgent': "Use mirroring technique: 'I understand you're frustrated...'",
            'suggestion': "I apologize for the inconvenience. I'm here to help resolve this situation in the best possible way.",
            'insight': "Customer in altered emotional state. Prioritize calming before negotiating (60%)",
            'probability': 60
        },
        'interested': {
            'suggestion': "Great! Let's work together to resolve this. What would be the best payment method for you?",
            'offer': "Receptive customer - can offer standard or better conditions",
            'insight': "Collaborative customer. Excellent probability of closing (90%)",
            'probability': 90
        },
        'needs_time': {
            'suggestion': "I understand. How much time would you need? We can schedule a callback or see installment options.",
            'offer': "Offer callback in 7-15 days or installments with smaller down payment",
            'insight': "Customer needs to organize finances. Medium probability with follow-up (70%)",
            'probability': 70
        },
        'disputes_debt': {
            'compliance': "ATTENTION: Customer disputes debt. Verify documentation before proceeding.",
            'urgent': "Request data for verification: CPF, address, recent purchases",
            'suggestion': "I'll verify this information. Can you confirm your CPF and address so I can check here?",
            'insight': "Debt dispute. Verification needed before negotiating (40%)",
            'probability': 40
        }
    },
    'pt': {
        'cant_pay': {
            'compliance': "Não mencione ação legal. Foque em soluções de pagamento.",
            'suggestion': "Entendo sua situação. Vamos encontrar uma solução que funcione para você. Que valor você conseguiria pagar mensalmente?",
            'offer': "Ofereça parcelamento em 6x ou desconto de 30% para pagamento à vista",
            'insight': "Cliente em dificuldade financeira. Alta probabilidade de aceitar parcelamento (75%)",
            'probability': 75
        },
        'wants_discount': {
            'suggestion': "Posso verificar que opções temos disponíveis. Para pagamento à vista, conseguimos oferecer condições especiais.",
            'offer': "Autorizado desconto até 40% para pagamento à vista ou 25% para pagamento em até 3x",
            'insight': "Cliente interessado em negociar. Probabilidade alta de fechamento (85%)",
            'probability': 85
        },
        'angry': {
            'compliance': "Cliente irritado. Mantenha tom calmo e empático. Não discuta.",
            'urgent': "Use técnica de espelhamento: 'Entendo que você está frustrado...'",
            'suggestion': "Peço desculpas pelo transtorno. Estou aqui para ajudar a resolver essa situação da melhor forma possível.",
            'insight': "Cliente em estado emocional alterado. Priorize acalmar antes de negociar (60%)",
            'probability': 60
        },
        'interested': {
            'suggestion': "Que bom! Vamos trabalhar juntos para resolver isso. Qual seria a melhor forma de pagamento para você?",
            'offer': "Cliente receptivo - pode oferecer condições padrão ou melhores",
            'insight': "Cliente colaborativo. Excelente probabilidade de fechamento (90%)",
            'probability': 90
        },
        'needs_time': {
            'suggestion': "Compreendo. Quanto tempo você precisaria? Podemos agendar um retorno ou ver opções de parcelamento.",
            'offer': "Ofereça callback em 7-15 dias ou parcelamento com entrada menor",
            'insight': "Cliente precisa organizar finanças. Probabilidade média com follow-up (70%)",
            'probability': 70
        },
        'disputes_debt': {
            'compliance': "ATENÇÃO: Cliente contesta dívida. Verifique documentação antes de prosseguir.",
            'urgent': "Solicite dados para verificação: CPF, endereço, últimas compras",
            'suggestion': "Vou verificar essas informações. Pode me confirmar seu CPF e endereço para eu consultar aqui?",
            'insight': "Contestação de dívida. Necessária verificação antes de negociar (40%)",
            'probability': 40
        }
    }
}

def get_language():
    """Get current language from session or default to Portuguese"""
    return session.get('language', 'pt')

def get_translation(key):
    """Get translation for current language"""
    lang = get_language()
    return TRANSLATIONS.get(lang, {}).get(key, key)

@app.route('/')
def index():
    return render_template('dashboard.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/live-call')
def live_call():
    return render_template('live_call.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/live-call-enhanced')
def live_call_enhanced():
    return render_template('live_call_enhanced.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/performance')
def performance():
    return render_template('performance.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/training')
def training():
    return render_template('training.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/settings')
def settings():
    return render_template('settings.html', 
                         lang=get_language(),
                         translations=TRANSLATIONS[get_language()],
                         languages=LANGUAGES)

@app.route('/set-language/<language>')
def set_language(language):
    if language in LANGUAGES:
        session['language'] = language
    return jsonify({'status': 'success', 'language': language})

@app.route('/api/ai-response', methods=['POST'])
def ai_response():
    data = request.get_json()
    message = data.get('message', '').lower()
    lang = get_language()
    
    # Determine response type based on message content
    response_type = 'default'
    
    if any(phrase in message for phrase in ['não tenho dinheiro', 'cant pay', 'no money']):
        response_type = 'cant_pay'
    elif any(phrase in message for phrase in ['desconto', 'discount']):
        response_type = 'wants_discount'
    elif any(phrase in message for phrase in ['irritado', 'angry', 'mad']):
        response_type = 'angry'
    elif any(phrase in message for phrase in ['interessado', 'interested']):
        response_type = 'interested'
    elif any(phrase in message for phrase in ['tempo', 'time']):
        response_type = 'needs_time'
    elif any(phrase in message for phrase in ['não devo', 'dispute', 'contest']):
        response_type = 'disputes_debt'
    
    # Get response template
    if response_type in AI_RESPONSES[lang]:
        response = AI_RESPONSES[lang][response_type]
    else:
        # Default response
        if lang == 'pt':
            response = {
                'suggestion': 'Entendo. Pode me explicar melhor sua situação para que eu possa ajudar da melhor forma?',
                'insight': 'Situação indefinida. Colete mais informações antes de fazer ofertas (50%)',
                'probability': 50
            }
        else:
            response = {
                'suggestion': 'I understand. Can you explain your situation better so I can help in the best way?',
                'insight': 'Undefined situation. Collect more information before making offers (50%)',
                'probability': 50
            }
    
    return jsonify({
        'status': 'success',
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard-data')
def dashboard_data():
    # Mock data for demonstration
    return jsonify({
        'daily_stats': {
            'calls_made': 19,
            'contacts_reached': 12,
            'payments_collected': 4,
            'collection_amount': 7500,
            'daily_goal_calls': 30,
            'daily_goal_collections': 10,
            'daily_goal_amount': 10000
        },
        'compliance_score': 95,
        'success_rate': 21.1,
        'avg_call_duration': 8.5,
        'recent_activities': [
            {
                'time': '14:30',
                'type': 'payment',
                'description': 'Payment collected - R$ 1,200',
                'status': 'success'
            },
            {
                'time': '14:15',
                'type': 'call',
                'description': 'Call completed - Customer interested',
                'status': 'success'
            },
            {
                'time': '14:00',
                'type': 'call',
                'description': 'Call completed - No contact',
                'status': 'warning'
            }
        ]
    })

@app.route('/api/customer-lookup', methods=['POST'])
def customer_lookup():
    data = request.get_json()
    cpf = data.get('cpf', '')
    name = data.get('name', '')
    
    # Mock customer data
    return jsonify({
        'status': 'success',
        'customer': {
            'name': 'João Silva Santos',
            'cpf': '123.456.789-00',
            'phone': '(11) 99999-9999',
            'email': 'joao.silva@email.com',
            'debt_amount': 2500.00,
            'days_overdue': 45,
            'payment_history': 'Good',
            'risk_score': 'Medium',
            'last_contact': '2024-01-10',
            'preferred_contact': 'Phone',
            'notes': 'Customer mentioned financial difficulties in last call'
        }
    })

@app.route('/api/payment-calculation', methods=['POST'])
def payment_calculation():
    data = request.get_json()
    debt_value = float(data.get('debt_value', 0))
    installments = int(data.get('installments', 1))
    discount = float(data.get('discount', 0))
    interest_rate = float(data.get('interest_rate', 0))
    
    # Calculate payment
    discounted_amount = debt_value * (1 - discount / 100)
    
    if installments == 1:
        installment_value = discounted_amount
    else:
        monthly_rate = interest_rate / 100
        if monthly_rate > 0:
            installment_value = discounted_amount * (monthly_rate * (1 + monthly_rate) ** installments) / ((1 + monthly_rate) ** installments - 1)
        else:
            installment_value = discounted_amount / installments
    
    total_amount = installment_value * installments
    
    return jsonify({
        'status': 'success',
        'calculation': {
            'original_amount': debt_value,
            'discount_amount': debt_value - discounted_amount,
            'discounted_amount': discounted_amount,
            'installment_value': installment_value,
            'total_amount': total_amount,
            'installments': installments
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

