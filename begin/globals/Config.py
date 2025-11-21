import os
import itsdangerous

##
class Config:
    SECRET_KEY = os.urandom(20)

serializer = itsdangerous.URLSafeSerializer(Config.SECRET_KEY)
