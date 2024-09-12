from flask import Flask, jsonify
import requests
import xmltodict

app = Flask(__name__)

PODCAST_URL = 'https://anchor.fm/s/49f0c604/podcast/rss'

def fetch_podcast_data():
    try:
        # Fazendo a requisição para o feed RSS
        response = requests.get(PODCAST_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o feed RSS: {e}")
        return None

def parse_podcast_data(xml_text):
    # Converte o XML em um dicionário usando xmltodict
    podcast_dict = xmltodict.parse(xml_text)
    items = podcast_dict['rss']['channel']['item']

    podcast_data = []
    for item in items:
        title = item['title']
        enclosure_url = item['enclosure']['@url']
        image_url = item.get('itunes:image', {}).get('@href', 'Imagem indisponível')

        podcast_data.append({
            'title': title,
            'enclosureUrl': enclosure_url,
            'imageUrl': image_url
        })

    return podcast_data

@app.route('/podcast', methods=['GET'])
def get_podcast():
    # Busca e analisa os dados do podcast
    xml_text = fetch_podcast_data()
    
    if not xml_text:
        return jsonify({'error': 'Erro ao buscar o feed do podcast'}), 500

    podcast_data = parse_podcast_data(xml_text)
    
    # Retorna os dados do podcast em formato JSON
    return jsonify(podcast_data)

if __name__ == '__main__':
    app.run(debug=True)
