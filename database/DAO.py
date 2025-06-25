from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select distinct t.year
from lahmansbaseballdb.teams t 
where t.year > 1979 """

        cursor.execute(query)

        results = []
        for row in cursor:
            results.append(row["year"])

        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def getSquadre(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select distinct t.name, t.teamCode
from lahmansbaseballdb.teams t 
where t.year = %s """

        cursor.execute(query,(anno,))

        results = []
        for row in cursor:
            results.append(f"{row["name"]} - {row["teamCode"]}")

        cursor.close()
        cnx.close()
        return results


    @staticmethod
    def getNodi(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select t.name, t.teamCode as ID, sum(s.salary) as totale
            from lahmansbaseballdb.salaries s, lahmansbaseballdb.teams t, lahmansbaseballdb.appearances a
            where s.`year` = t.`year` and t.`year` = a.`year` 
            and a.`year` = %s
            and t.ID = a.teamID 
            and s.playerID = a.playerID 
            group by t.teamCode, t.name """

        cursor.execute(query,(anno, ))

        results = []
        for row in cursor:
            results.append(Team(**row))

        cursor.close()
        cnx.close()
        return results
