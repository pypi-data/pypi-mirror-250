from pluralizer import Pluralizer
import caseswitcher
import secrets

pz = Pluralizer()

def lcase(x): return x[0].lower() + x[1:]
def joinify(column_name, item_list): return ','.join(i[column_name] for i in item_list)
def pluralize(x): return pz.pluralize(x)
def camel(x): return caseswitcher.to_camel(x)
def kebab(x): return caseswitcher.to_kebab(x)
def pascale(x): return caseswitcher.to_pascal(x)
def dot(x): return caseswitcher.to_dot(x)
def title(x): return caseswitcher.to_title(x)
def snake(x): return caseswitcher.to_snake(x)
def path(x): return caseswitcher.to_path(x)
def uuid(): return str(uuid.uuid4())
def secret(): return secrets.token_hex(16)
def secret_complex(): return secrets.token_hex(64)