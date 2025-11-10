[app]
title = Okit AI
package.name = okitai
package.domain = com.okitai

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

version = 2.0.0
requirements = python3,kivy==2.3.0,requests,google-generativeai,pillow

orientation = portrait

[buildozer]
log_level = 2

presplash.filename = assets/wolf_icon.png
icon.filename = assets/icon.png

android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Utiliser des versions plus récentes et stables
android.api = 31
android.minapi = 21
android.sdk = 21
android.ndk = 23b

# Build tools plus récents
android.build_tools = 30.0.3

android.allow_backup = True
android.gradle_dependencies = com.google.android.gms:play-services-auth:20.7.0

# Accepter automatiquement les licences
android.accept_sdk_license = True

p4a.branch = develop
