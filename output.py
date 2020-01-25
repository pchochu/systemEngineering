from datetime import datetime

def createOutput(totalNumOfPeople, unsatisfiedPeople, numberOfPlacesAtTablesF, numberOfPlacesAtEAndGChairs):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    with open(('Results_' + time), 'a') as output:
        output.write('Total number of people that visited the system: ' + str(totalNumOfPeople) + '\n' )
        output.write('Total number of people that were not able to find a place: ' + str(unsatisfiedPeople) + '\n' )
        output.write('Total number of places at tables: ' + str(numberOfPlacesAtTablesF) + '\n' )
        output.write('Total number of places at chairs at bars: ' + str(numberOfPlacesAtEAndGChairs) + '\n' )

        output.close()
