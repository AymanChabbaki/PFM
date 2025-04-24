from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

app = Flask(__name__)
CORS(app)

# Load model and preprocessing artifacts
model = joblib.load('C:/Users/HP/Desktop/myPfm/catboost_model.pkl')
preprocessor = joblib.load('C:/Users/HP/Desktop/myPfm/preprocessor.pkl')
transformed_features = joblib.load('C:/Users/HP/Desktop/myPfm/transformed_features.pkl')

# Get known categories from the encoder
cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
known_categories = {
    'marque': cat_encoder.categories_[0].tolist(),
    'type de carburant': cat_encoder.categories_[1].tolist(),
    'modèle': cat_encoder.categories_[2].tolist(),
    'Transmision': cat_encoder.categories_[3].tolist()
}


# Create a mapping of brand to models from your training data
# (You'll need to extract this from your original DataFrame)
brand_model_map = {
'alfa-romeo': ['giulietta', 'autre', 'stelvio', 'tonale', 'giulia', '166', '147', 'mito', '156', '159', '146'], 'audi': ['a5', 'q3', 'a4', 'a3', 'a6', 'q5', 'a1', 'q2', 'a7', 'q7', 'tt', 'autre', '80'], 'bmw': ['serie 2', 'serie 3', 'serie 1', 'serie 4', 'x5', 'serie 5', 'x3', 'x4', 'x1', 'serie 7', 'x6', 'x2', 'autre', 'z4'], 'citroen': ['c5', 'berlingo', '2 cv', 'c3', 'c4', 'c-elysee', 'ami', 'c15', 'autre', 'c1', 'xsara', 'jumper', 'nemo', 'c8', 'c2', 'spacetourer', 'saxo', 'c-crosser', 'zx', 'jumpy'], 
'dacia': ['sandero', 'lodgy', 'dokker', 'duster', 'logan', 'autre'], 'fiat': ['tipo', '500', '500x', '500l', 'freemont', 'fiorino', 'doblo', 'autre', 'palio', 'panda', 'punto', 'ducato', 'fullback', 'uno', 'albea', 'siena', 'grande punto', 'linea', 'bravo', 'brava', '500c', 'scudo', 'ulysse', 'stilo'], 'ford': ['c max', 'fiesta', 'kuga', 'ecosport', 'focus', 'ranger', 'mustang', 'fusion', 'transit', 'f-250', 'ka', 'tourneo connect', 'courrier', 'autre', 'mondeo', 'connect', 'b max', 'tourneo custom', 'escort', 's-max', 'galaxy', 'f-150', 'cougar'], 'honda': ['cr-v', 'hr-v', 'civic', 'city', 'accord', 'jazz', 'cr-x'], 'hyundai': ['tucson', 'creta', 'accent', 'santa fe', 'i30', 'i20', 'elantra', 'autre', 'i10', 'kona', 'ix35', 'i40', 'h350', 'h1', 'atos', 'h100', 'genesis', 'trajet', 'veracruz', 'matrix', 'terracan', 'sonata', 'ioniq', 'ix55', 'galloper'], 'kia': ['picanto', 'sportage', 'sorento', 'seltos', 'ceed', 'rio', 'carens', 'cerato', 'soul', 'k5', 'k2700', 'optima', 'carnival', 'sonet', 'proceed', 'niro hybride'], 'land-rover': ['discovery', 'range rover evoque', 'range rover', 'discovery sport', 'defender', 'range rover sport', 'range rover velar', 'freelander'], 'mercedes-benz': ['classe a', 'classe c', '220', 'classe e', 'classe glc', 'classe cla', 'classe gla', 'classe glk', '270', 'amg gts', 'classe ml', 'vito', '180', 'classe b', 'viano', '210', '190', '200', '250', 'classe gle', 'classe clk', 'classe clc', 'sprinter', '310d', '207d', 'citan', 'classe slk', 'classe cls', '240', 'classe v', 'classe s', '300', '230'], 'nissan': ['qashqai', 'juke', 'micra', 'navara', 'x trail', 'note', 'pathfinder', 'pick-up', 'tiida', 'primera', 'sunny', 'terrano', 'evalia'], 'opel': ['astra', 'grandland', 'insignia', 'corsa', 'adam', 'crossland', 'mokka', 'zafira', 'antara', 'gt', 'combo', 'meriva', 'vectra', 'movano'], 'other': ['cooper', 'f-pace', 'spark', 'captiva', 'renegade', 'cherokee', 'xe', 'xc60', '595', 'swift', 'ghibli', 'stavic', 'autre', 'wrangler', 'tiggo', 'ds5', 'glory 580', 'compass', 'glory ix5', 'countryman', 'e-pace', 'mg5', 'rexton', 'tiggo 7 pro', 'xc90', 'xf', 'xc40', 's90', 'formentor', '2', 's60', 'v40', 'grand cherokee', 'lancer', 'sirion', 'ds7', 'cruze', 'alto', 'korando', 'ignis', 'maruti', '320', 'l200', 'delta', 'sportero', 'actyon', '3', 'daily', 'qq', 'sx-4', 'es', 'celerio', '6', 'kyron', 'grand vitara', 'xj', 'rascal', 'labo', 'lanos', 'optra', 'nexia', '75', '2008', 'splash', 'd-max', 'one', 'tiggo 4 pro', 'carry', 'c30', 'escalade', 'aveo', 'haval', 'super cab', 'ds4', 'nomad', '323', 'kuv 100', 'pajero sport', 'serie 400', 'colt', 'k01h', 'vitara', 'outlander', 'next', 'k01s', 's40', 'pik-up', '1308 gt', 'cayenne', 'cabrio', 'ypsilon', 'minyi', '1301', 'k01l', 'cx7', 'paceman', 'ds3', 'pickup', 'forfour', 'avenger', 'type x', 'ateca', 'jimny', 'benni', 'hover', 'cmp', 'pajero', 'challenger', 'a5', 'wagon r', 'caliber', 'l300', 'cx-5', '124 spider', 'zs', 'leon', 'cross country', 'canter', 'f3', 'legacy', 'alsvin', 'fortwo', 'fc', 'super ace', 'mx3', 'tm', 's80', 'patriot', 'clubman', 'mx5', 'brabus', 'terios', 'mg 3', 'ck', 'tiggo 2 pro', 'mpv', '695', 'a113', '626', 'premacy', 'panamera', 'grandis'], 'peugeot': ['508', '3008', '208', '2008', 'expert', '308', '5008', '301', '206', '407', '307', '306', 'boxer', '106', '207', '406', '309', 'rifter', '205', 'autre', 'partner', 'bipper', 'pick up', '807', '4008', '107', '108', '607', 'landtrek', '405', '4007'], 'renault': ['megane', 'captur', 'megane 4', 'clio', 'express', 'kadjar', 'arkana', 'kangoo', 'koleos', 'laguna', 'r4', 'zoe', 'twingo', 'scenic', 'master', 'symbol', 'r19', 'talisman', 'trafic', 'latitude', 'fluence', 'grand scenic', 'samsung sm3', 'espace', 'super 5', 'nevada', 'autre'], 'seat': ['ateca', 'ibiza', 'altea', 'toledo', 'leon', 'altea xl', 'arona', 'cordoba', 'exeo'], 'skoda': ['superb', 'octavia', 'kamiq', 'fabia', 'kodiaq', 'karoq', 'rapid', 'roomster', 'yeti', 'autre', 'scala'], 'toyota': ['yaris', 'corolla cross', 'corolla', 'c-hr', 'hilux', 'auris', 'rav-4', '4runner', 'fortuner', 'corolla verso', 'tercel', 'avensis', 'aygo', 'verso', 'celica', 'prado', 'starlet', 'prius', 'land cruiser', 'fj cruiser'], 'volkswagen': ['passat', 'touareg', 'touran', 'polo', 'tiguan', 'coccinelle', 'golf 7', 't-roc', 'eos', 'caddy', 'golf 8', 'jetta', 'golf 6', 'new golf', 'passat cc', 'golf 5', 'golf 4', 'arteon', 'gol', 'vento', 'transporter', 'fox', 'amarok', 'golf 3', 'sharan', 'crafter', 'bora', 'scirocco', 'new beetle', 'caravelle', 'thing', 'taigo', 'golf 1', 'golf 2']}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = {
            'marque': 'Marque',
            'modele': 'Modèle',
            'transmission': 'Transmission',
            'puissance_fiscale': 'Puissance fiscale',
            'carburant': 'Carburant',
            'kilometrage': 'Kilométrage',
            'annee': 'Année'
        }
        
        # Check for missing fields
        missing_fields = [french for eng, french in required_fields.items() 
                        if eng not in data or not data[eng]]
        if missing_fields:
            return jsonify({'error': f'Champs manquants: {", ".join(missing_fields)}'}), 400

        # Validate categories
        validation_errors = []
        
        if data['marque'] not in known_categories['marque']:
            validation_errors.append(f"Marque inconnue: {data['marque']}")
        if data['modele'] not in known_categories['modèle']:
            validation_errors.append(f"Modèle inconnu: {data['modele']}")
        if data['transmission'] not in known_categories['Transmision']:
            validation_errors.append(f"Transmission inconnue: {data['transmission']}")
       # In your /predict endpoint, modify the carburant validation:
        received_carburant = data['carburant'].strip()  # Clean whitespace
        known_fuels = [f.strip() for f in known_categories['type de carburant']]

        if received_carburant not in known_fuels:
            validation_errors.append(
                f"Carburant inconnu: {received_carburant}. "
                 f"Options valides: {known_fuels}"
                    )
            
        if validation_errors:
            return jsonify({'error': " | ".join(validation_errors)}), 400

        # Prepare input data
        input_data = {
            'marque': [data['marque']],
            'modèle': [data['modele']],
            'Transmision': [data['transmission']],
            'type de carburant': [data['carburant']],
            'puissance fiscale': [int(data['puissance_fiscale'])],
            'kilométrage': [int(data['kilometrage'])],
            'année': [int(data['annee'])]
        }
        
        input_df = pd.DataFrame(input_data)
        
        try:
            processed_data = preprocessor.transform(input_df)
            processed_df = pd.DataFrame(processed_data, columns=transformed_features)
            prediction = model.predict(processed_df)[0]
            return jsonify({'price': round(float(prediction))})
        except Exception as e:
            return jsonify({'error': f"Erreur de traitement: {str(e)}"}), 400
            
    except Exception as e:
        return jsonify({'error': f"Erreur du serveur: {str(e)}"}), 500

@app.route('/marques', methods=['GET'])
def get_marques():
    return jsonify({'marques': known_categories['marque']})
@app.route('/modeles', methods=['GET'])
def get_modeles():
    marque = request.args.get('marque')
    if not marque:
        return jsonify({'error': 'Paramètre marque requis'}), 400

    # Debug prints
    print(f"\nRequest for marque: {marque}")
    print("All brands in map:", brand_model_map.keys())
    
    # Find matching brand (case insensitive)
    marque_lower = marque.lower()
    matching_brand = next((b for b in brand_model_map.keys() 
                         if b.lower() == marque_lower), None)
    
    if not matching_brand:
        print(f"Brand '{marque}' not found in map")
        return jsonify({'modeles': []})
    
    all_models = brand_model_map[matching_brand]
    print(f"All models for {marque}: {all_models}")
    print(f"Known models: {known_categories['modèle']}")
    
    # Create lowercase versions for comparison
    known_models_lower = [m.lower() for m in known_categories['modèle']]
    
    # Find matches with flexible comparison
    valid_models = []
    for model in all_models:
        model_lower = model.lower()
        # Check direct match or contains relationship
        if (model_lower in known_models_lower or
            any(model_lower in m.lower() for m in known_categories['modèle']) or
            any(m.lower() in model_lower for m in known_categories['modèle'])):
            valid_models.append(model)
    
    print(f"Valid models found: {valid_models}")
    return jsonify({'modeles': valid_models})

@app.route('/debug_models', methods=['GET'])
def debug_models():
    return jsonify({
        'brand_model_map_sample': brand_model_map.get('ford', []),
        'known_models_sample': known_categories['modèle']
    })
@app.route('/debug_fuel_types', methods=['GET'])
def debug_fuel_types():
    return jsonify({
        'known_fuel_types': known_categories['type de carburant']
    })
if __name__ == '__main__':
    app.run(debug=True, port=5000)