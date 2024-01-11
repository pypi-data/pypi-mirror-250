#### What is this?

Genmax is a simple code generation tool.

#### Extensions supported in templates

The following methods are supported in the template:

| Description | Method |
|:---|:---|
|Lower case| lcase(your_string)|
|Pluralize| pluralize(your_string)|
|Join With Commas| joinify(name_of_element, element_list)|
|Switch to Camel case| camel(your_string)|
|Switch to Kebab case| kebab(your_string)|
|Switch to Pascale case| pascale(your_string)|
|Switch to Dot case| dot(your_string)|
|Switch to Title case| title(your_string)|
|Switch to Snake case| snake(your_string)|
|Switch to Path format| path(your_string)|
|Generate UUID| uuid()|
|Generate secret in 16 bit - hexadecimal| secret()|
|Generate secret in 64 bit - hexadecimal| secret_complex()|

#### Run It

```bash
python main.py asp asp_web
```