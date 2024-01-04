from peewee import *
from dotenv import dotenv_values

db_configs = dotenv_values('env/app.env')

db = PostgresqlDatabase(
    db_configs['DB_NAME'],
    user=db_configs['DB_USER'],
    password=db_configs['DB_PASSWORD'],
    host=db_configs['DB_HOST'],
    port=db_configs['DB_PORT']
)


class BaseModel(Model):
    class Meta:
        database = db


class ListOfBuilders(BaseModel):
    id = AutoField()

    name = TextField(null=False)
    info = TextField(null=False)
    foundation_year = IntegerField(null=False)
    completed_projects = IntegerField(null=False)
    projects_in_process = IntegerField(null=False)
    trusted = BooleanField(null=False)

    info__lang_hebrew = TextField(null=False)

    class Meta:
        db_table = "ListOfBuilders"
        order_by = ('id')


class ListOfBuildings(BaseModel):
    id = AutoField()
    group_id = IntegerField(null=False)

    name = TextField(null=False)
    info = TextField(null=False)
    country = TextField(null=False)
    city = TextField(null=False)
    address = TextField(null=False)
    parking = IntegerField(null=False)
    type_of_building = TextField(null=False)
    coord_x = FloatField(null=False)
    coord_y = FloatField(null=False)

    city__lang_hebrew = TextField(null=False)
    country__lang_hebrew = TextField(null=False)
    address__lang_hebrew = TextField(null=False)
    info__lang_hebrew = TextField(null=False)

    class Meta:
        db_table = "ListOfBuildings"
        order_by = ('id')


class ListOfFlats(BaseModel):
    id = AutoField()
    group_id = IntegerField(null=False)

    info = TextField(null=False)
    price = IntegerField(null=False)
    price_per_m2 = IntegerField(null=False)
    rooms = IntegerField(null=False)
    floor = IntegerField(null=False)
    all_size_m2 = IntegerField(null=False)
    kitchen_size_m2 = IntegerField(null=False)
    bathroom_size_m2 = IntegerField(null=False)
    hall_size_m2 = IntegerField(null=False)
    inside_size_m2 = IntegerField(null=False)

    info__lang_hebrew = TextField(null=False)

    class Meta:
        db_table = "ListOfFlats"
        order_by = ('id')


class ListOfImages(BaseModel):
    id = AutoField()
    type = TextField(null=False)
    group_id = IntegerField(null=False)
    file_name = TextField(null=False)

    class Meta:
        db_table = "ListOfImages"
        order_by = ('id')


class ListOfUsers(BaseModel):
    id = AutoField()
    login = TextField(null=False, unique=True)
    password = TextField(null=False)
    role = TextField(null=False, default='user')

    class Meta:
        db_table = "ListOfUsers"
        order_by = ('id')


MODELS = {
    'ListOfBuilders': ListOfBuilders,
    'ListOfBuildings': ListOfBuildings,
    'ListOfFlats': ListOfFlats,
    'ListOfImages': ListOfImages,
    'ListOfUsers': ListOfUsers,
}
