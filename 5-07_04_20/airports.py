class Airports(object):
    def __init__(self):
        pass

    def get_airport_by_iata(self, iata_code, db):
        try:
            airportName = db.get().to_dict().get('airportName')
            return airportName
        except:
            return None
