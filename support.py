from csv import DictReader, reader
from cs50 import SQL
from helpers import get

if __name__ == '__main__':
    
    
    db = SQL('sqlite:///nbs.db')
    
    artist = 'BLACKPINK'
    chart = "ind"
    month = "nov_dec"
    
    info = get(artist, chart, month)
    exe = db.execute(info)
    
    print(exe)
    
    # Open the csv file
    with open('cmb.csv', 'r') as file:
        reader = DictReader(file)
        infos = list(reader)
    
    for info in infos:
        artist_id = db.execute('SELECT id FROM nbs WHERE artist = ?', info['artist'])[0]['id']
        jan = info['jan']
        feb = info['feb']
        mar = info['mar']
        apr = info['apr']
        may = info['may']
        jun = info['jun']
        jul = info['jul']
        aug = info['aug']
        sep = info['sep']
        oct = info['oct']
        nov_dec = info['nov-dec']
        db.execute('INSERT INTO cmb (artist_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov_dec) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', artist_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov_dec)
    

    # Open the csv file
    with open('smi.csv', 'r') as file:
        reader = DictReader(file)
        infos = list(reader)
    
    for info in infos:
        artist_id = db.execute('SELECT id FROM nbs WHERE artist = ?', info['artist'])[0]['id']
        jan = info['jan']
        feb = info['feb']
        mar = info['mar']
        apr = info['apr']
        may = info['may']
        jun = info['jun']
        jul = info['jul']
        aug = info['aug']
        sep = info['sep']
        oct = info['oct']
        nov_dec = info['nov-dec']
        db.execute('INSERT INTO smi (artist_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov_dec) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', artist_id, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov_dec)
    
    
    
    # Open the csv file
    with open('nbs.csv', 'r') as file:
        reader = DictReader(file)
        infos = list(reader)
    
    for info in infos:
        artist = info['artist']
        smi = info['smi']
        cmb = info['cmb']
        index = info['index']
        db.execute('INSERT INTO nbs (artist, smi, cmb, ind) VALUES (?, ?, ?, ?)', artist, smi, cmb, index)
        
