from tortoise import fields, Model


class Game(Model):
    id = fields.IntField(pk=True, generated=True)
    title = fields.CharField(max_length=128)
    slug = fields.CharField(max_length=256)
    description = fields.TextField(null=True)
    genre = fields.CharField(max_length=24, null=True)
    platform = fields.CharField(max_length=16)
    metacritic = fields.IntField(null=True)
    release_date = fields.DateField(null=True)
    background_image = fields.CharField(max_length=512, null=True)
    torrent = fields.BooleanField(null=True)


class GameScreens(Model):
    game = fields.ForeignKeyField('models.Game', on_delete=fields.CASCADE)
    short_screenshot = fields.CharField(max_length=256)


class TorrentComment(Model):
    id = fields.IntField(pk=True, generated=True)
    user = fields.CharField(max_length=256)
    game = fields.ForeignKeyField('models.Game', on_delete=fields.CASCADE)
    text = fields.CharField(max_length=256)
    value = fields.IntField(default=0)
    date = fields.CharField(max_length=128)


class TorrentCommentLikes(Model):
    comment = fields.ForeignKeyField('models.TorrentComment', on_delete=fields.CASCADE)
    user_id = fields.IntField()
    value = fields.IntField()


class Torrent(Model):
    name = fields.CharField(max_length=128)
    game = fields.ForeignKeyField('models.Game', on_delete=fields.CASCADE)
    magnet = fields.TextField()
    file_size = fields.CharField(max_length=32)
    seeders = fields.IntField()


class User(Model):
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=32)
    email = fields.CharField(max_length=64)
    password = fields.CharField(max_length=64)
    role = fields.IntField()
    refresh = fields.CharField(max_length=1000, null=True)

