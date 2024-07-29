from argostranslate import package

languages = [
    'en',
    'es',
    'el',
    'de',
    'it',
    'pt',
    'pl',
    'ru',
    'fr',
]

packages = package.get_available_packages()
for pkg in packages:
    if pkg.from_code in languages and pkg.to_code in languages:
        print(f"Downloading Argos package {pkg} skipped...")
        # package.install_from_path(pkg.download())
