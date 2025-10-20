[app]
title = Customers
package.name = customers
package.domain = org.example
source.dir = .
source.include_exts = py,xlsx
version = 1.0.0
orientation = portrait
fullscreen = 0

# Kivy/KivyMD + Excel support
requirements = python3,kivy==2.2.1,kivymd==1.1.1,openpyxl==3.1.5,et-xmlfile,pyjnius

# Android settings
android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.use_androidx = True

# Release signing (fill values or use env vars)
# Keystore path relative to project root (create with keytool)
android.release_keystore = %(source.dir)s/keystore/release.keystore
# Key alias created inside the keystore
android.release_keyalias = customerskey
# Keystore and alias passwords (prefer env vars over storing here)
# android.release_keystore_pass = YOUR_KEYSTORE_PASSWORD
# android.release_keyalias_pass = YOUR_KEY_ALIAS_PASSWORD

# Optional: keep logs readable
log_level = 2

[buildozer]
warn_on_root = 1
log_level = 2