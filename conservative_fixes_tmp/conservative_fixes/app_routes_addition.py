# ADD THESE ROUTES TO YOUR EXISTING app.py
# Just copy and paste these routes at the end of your app.py file

@app.route('/training')
def training():
    lang = session.get('lang', 'pt')
    translations = get_translations()
    return render_template('training.html', lang=lang, translations=translations)

@app.route('/performance')
def performance():
    lang = session.get('lang', 'pt')
    translations = get_translations()
    return render_template('performance.html', lang=lang, translations=translations)

@app.route('/live-call')
def live_call():
    lang = session.get('lang', 'pt')
    translations = get_translations()
    return render_template('live_call.html', lang=lang, translations=translations)

