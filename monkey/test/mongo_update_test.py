from scripts.external.report import update_section
from scripts.connection.mongo_db.crud import load_by_id_from_mongodb
from scripts.format import SectionData


# data = load_by_id_from_mongodb(col='monkey_section', id='64f9651537ea1b3c47b1347a')
# print(data)

id = input()
update_section(id, SectionData(
    start_time=1,
    end_time=2,
))
print(id)