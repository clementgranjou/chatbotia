
import json
from llamatest import *



from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
import llamatest
app = Flask(__name__)
 
# Définir la clé secrète
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'
 
# Fonction pour vérifier le token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Token')  # http://127.0.0.1:5000/route?token=xxxxxxx

        if not token:
            print("no token")
            return jsonify({'message': 'Token is missing!, no token'}), 403
 
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
 
        return f(*args, **kwargs)
 
    return decorated
 
# Route pour générer le token JWT
@app.route('/login')
def login():
    # Générer le token avec une expiration de 3 jours
    token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3)
    }, app.config['SECRET_KEY'], algorithm="HS256")
 
    return jsonify({'token': token})
 
# Route protégée
@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Ceci est seulement accessible avec un token valide.'})
 
 
 
# Route protégée
@app.route('/bot', methods=['POST'])
@token_required
def process_input():
    # Vérifie si le corps de la requête contient du JSON
    if request.is_json:
        # Récupère les données JSON du corps de la requête
        data = request.get_json()
        
        # Récupère la valeur du champ 'input' dans les données JSON
        input_value = data.get('input', None)  # Retourne None si 'input' n'existe pas
        
        if input_value is not None:
            # Traitement avec 'input_value'
            response = bot_answer(input_value)
            return response
            # jsonify({'message': 'Input reçu', 'input': input_value})
        else:
            return jsonify({'message': 'Champ "input" manquant'}), 400
    else:
        return jsonify({'message': 'Le corps de la requête doit être du JSON'}), 400
 
 
 
 

 
if __name__ == '__main__':
    app.run(debug=True)