from flask import Flask, request, render_template
from scraping.dash_app import setup_dash


app = Flask(__name__)



    
    
@app.route('/')
def hello_world():
   return "<h1>hello world</h1>"
  
  
@app.route('/scrape/<module>')
def scraper(module):
    nb = request.args.getlist('args')
    # data = data_scraper(module, nb) 
    return 'data'


# df_reviews = data_scraper('drugs', )
setup_dash(app, [100]) 
 
def main():
    app.run(debug=True)

if __name__ == '__main__':
     main()