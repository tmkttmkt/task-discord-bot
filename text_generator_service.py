import sys
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

# data モジュールをインポート
sys.path.append('/app/src')
from data.main import Tetsu, Fumu

class TextGeneratorHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.text_generator = None
        self.initialize_generator()
        super().__init__(*args, **kwargs)
    
    def initialize_generator(self):
        try:
            f = Fumu(num=1)
            data_path = Path('/app/data/output2.json')
            if data_path.exists():
                f.read_json(data_path)
                self.text_generator = Tetsu(f.date)
                print("テキスト生成器が正常に初期化されました")
            else:
                print(f"データファイルが見つかりません: {data_path}")
        except Exception as e:
            print(f"テキスト生成器の初期化に失敗しました: {e}")
    
    def do_GET(self):
        if self.path == '/generate':
            self.handle_generate()
        elif self.path == '/health':
            self.handle_health()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        if self.path == '/generate':
            self.handle_generate()
        else:
            self.send_error(404, "Not Found")
    
    def handle_generate(self):
        try:
            if self.text_generator is None:
                self.send_json_response({
                    'error': 'テキスト生成器が利用できません',
                    'text': None
                }, 500)
                return
            
            generated_text = self.text_generator.create_text()
            self.send_json_response({
                'text': generated_text,
                'success': True
            })
        except Exception as e:
            self.send_json_response({
                'error': str(e),
                'text': None
            }, 500)
    
    def handle_health(self):
        status = "OK" if self.text_generator is not None else "ERROR"
        self.send_json_response({
            'status': status,
            'service': 'text-generator',
            'mecab_available': True
        })
    
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TextGeneratorHandler)
    print(f"テキスト生成サービスを http://localhost:{port} で開始します")
    print("利用可能なエンドポイント:")
    print(f"  GET/POST http://localhost:{port}/generate - テキスト生成")
    print(f"  GET http://localhost:{port}/health - ヘルスチェック")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nサービスを停止しています...")
        httpd.shutdown()

if __name__ == '__main__':
    port = int(os.getenv('TEXT_GENERATOR_PORT', 8080))
    run_server(port)